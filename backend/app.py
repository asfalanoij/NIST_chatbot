import hmac
import json
import logging
import re
from functools import wraps
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

from agents import Orchestrator
from ingest import ingest_documents
from visitor_tracker import track_visit, get_visitor_counts, check_db_health
from rag_engine import get_llm_backend_name
from crossmap import get_crossmap, get_families, get_stats, generate_sankey_csv
from interaction_log import get_stats as get_interaction_stats

load_dotenv()

app = Flask(__name__)

# Reject bodies larger than 16 KB — prevents oversized payload abuse (T07)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

# CORS: use env var or default to localhost dev origins
cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:5050")
CORS(app, origins=[o.strip() for o in cors_origins.split(",")])

# Flask config from env
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")

# Rate limiting — protects Gemini API costs
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

_INTERNAL_ERROR_MSG = "An internal error occurred. Please try again."


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Rate limit exceeded. Please try again later.", "retry_after": e.description}), 429


@app.errorhandler(413)
def payload_too_large(e):
    return jsonify({"error": "Request payload too large."}), 413


# Initialize Orchestrator
orchestrator = Orchestrator()


# --- Security Headers ---
@app.after_request
def set_security_headers(response: Response) -> Response:
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    if not app.debug:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# --- API Key Authentication ---
def require_api_key(f):
    """Decorator to require X-API-Key header on protected endpoints."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = os.environ.get("API_KEY")
        # If no API_KEY is configured, skip auth (dev mode)
        if not api_key:
            return f(*args, **kwargs)
        provided = request.headers.get("X-API-Key", "")
        # Constant-time comparison prevents timing attacks (C3)
        if not provided or not hmac.compare_digest(provided, api_key):
            return jsonify({"error": "Unauthorized. Provide a valid X-API-Key header."}), 401
        return f(*args, **kwargs)
    return decorated


def _sanitise_session_id(raw: str) -> str:
    """Strip non-alphanumeric chars and truncate to 64 chars (M2)."""
    return re.sub(r'[^a-zA-Z0-9\-_]', '', raw)[:64]


@app.before_request
def track_visitor():
    """Log visitor on API chat requests."""
    if request.path == "/api/chat" and request.method == "POST":
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ua = request.headers.get("User-Agent", "")
        track_visit(ip_address=ip, user_agent=ua, path=request.path)


@app.route('/api/health', methods=['GET'])
def health_check():
    db_ok = check_db_health()
    faiss_ok = os.path.exists(orchestrator.rag_engine.index_path)

    status = "healthy" if db_ok and faiss_ok else "degraded"
    return jsonify({
        "status": status,
        "service": "nist-chatbot-orchestrator",
        "checks": {
            "database": "ok" if db_ok else "unavailable",
            "faiss_index": "ok" if faiss_ok else "missing",
        },
    }), 200


@app.route('/api/chat', methods=['POST'])
@limiter.limit("10/minute")
@require_api_key
def chat():
    data = request.json
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    question = data.get('message')
    history = data.get('history', [])
    session_id = _sanitise_session_id(request.headers.get("X-Session-ID", ""))

    if not question:
        return jsonify({"error": "Message is required"}), 400

    if len(question) > 2000:
        return jsonify({"error": "Message too long. Maximum 2000 characters."}), 400

    try:
        response = orchestrator.route_and_chat(question, history, session_id=session_id)
        return jsonify(response)
    except Exception:
        logger.exception("Unhandled error in /api/chat")
        return jsonify({"error": _INTERNAL_ERROR_MSG}), 500


@app.route('/api/chat/stream', methods=['POST'])
@limiter.limit("10/minute")
@require_api_key
def chat_stream():
    """SSE streaming endpoint for incremental answer delivery."""
    data = request.json
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    question = data.get('message')
    history = data.get('history', [])
    session_id = _sanitise_session_id(request.headers.get("X-Session-ID", ""))

    if not question:
        return jsonify({"error": "Message is required"}), 400

    if len(question) > 2000:
        return jsonify({"error": "Message too long. Maximum 2000 characters."}), 400

    def generate():
        try:
            yield from orchestrator.route_and_chat_stream(
                question=question,
                history=history,
                session_id=session_id,
            )
        except Exception:
            logger.exception("Unhandled error in /api/chat/stream")
            # C2: use json.dumps — never interpolate exception string into SSE
            yield f"data: {json.dumps({'error': 'Stream error. Please try again.'})}\n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.route('/api/ingest', methods=['POST'])
@limiter.limit("5/minute")
@require_api_key
def run_ingest():
    """Triggers the ingestion process for documents in the docs/ folder."""
    if os.environ.get("DISABLE_INGEST", "").lower() == "true":
        return jsonify({"error": "Ingestion is disabled in production."}), 403
    try:
        stats = ingest_documents()
        return jsonify({"status": "success", "stats": stats}), 200
    except Exception:
        logger.exception("Unhandled error in /api/ingest")
        return jsonify({"error": _INTERNAL_ERROR_MSG}), 500


@app.route('/api/visitors/count', methods=['GET'])
def visitor_count():
    """Return visitor statistics."""
    try:
        counts = get_visitor_counts()
        return jsonify(counts), 200
    except Exception:
        logger.exception("Unhandled error in /api/visitors/count")
        return jsonify({"error": _INTERNAL_ERROR_MSG}), 500


# --- Interaction Stats Endpoint ---

@app.route('/api/interactions/stats', methods=['GET'])
@limiter.limit("60/minute")
@require_api_key
def interaction_stats():
    """Return aggregate interaction quality stats (admin only)."""
    try:
        stats = get_interaction_stats()
        return jsonify(stats), 200
    except Exception:
        logger.exception("Unhandled error in /api/interactions/stats")
        return jsonify({"error": _INTERNAL_ERROR_MSG}), 500


# --- Cross-Mapping Endpoints ---

@app.route('/api/crossmap', methods=['GET'])
def crossmap():
    """Return NIST 800-53 cross-mapping to ISO 27001, CSF 2.0, ISO 27005."""
    family = request.args.get('family')
    nist_id = request.args.get('nist_id')
    framework = request.args.get('framework')
    data = get_crossmap(family=family, nist_id=nist_id, framework=framework)
    return jsonify({"mappings": data, "count": len(data)}), 200


@app.route('/api/crossmap/families', methods=['GET'])
def crossmap_families():
    return jsonify({"families": get_families()}), 200


@app.route('/api/crossmap/stats', methods=['GET'])
def crossmap_stats():
    return jsonify(get_stats()), 200


@app.route('/api/crossmap/sankey', methods=['GET'])
def crossmap_sankey():
    csv_data = generate_sankey_csv()
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=nist_crossmap_sankey.csv'},
    )


if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', os.environ.get('PORT', 5050)))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)  # nosec B104
