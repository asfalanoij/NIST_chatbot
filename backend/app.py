from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from agents import Orchestrator
from ingest import ingest_documents
from visitor_tracker import track_visit, get_visitor_counts
from rag_engine import get_llm_backend_name

load_dotenv()

app = Flask(__name__)

# CORS: use env var or default to localhost dev origins
cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:5050")
CORS(app, origins=[o.strip() for o in cors_origins.split(",")])

# Flask config from env
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")

# Initialize Orchestrator
orchestrator = Orchestrator()


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
        if not provided or provided != api_key:
            return jsonify({"error": "Unauthorized. Provide a valid X-API-Key header."}), 401
        return f(*args, **kwargs)
    return decorated


@app.before_request
def track_visitor():
    """Log visitor on API chat requests."""
    if request.path == "/api/chat" and request.method == "POST":
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ua = request.headers.get("User-Agent", "")
        track_visit(ip_address=ip, user_agent=ua, path=request.path)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "nist-chatbot-orchestrator",
        "llm_backend": get_llm_backend_name(),
    }), 200


@app.route('/api/chat', methods=['POST'])
@require_api_key
def chat():
    data = request.json
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    question = data.get('message')
    history = data.get('history', [])

    if not question:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = orchestrator.route_and_chat(question, history)
        return jsonify(response)
    except Exception as e:
        print(f"Error processing chat: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/ingest', methods=['POST'])
@require_api_key
def run_ingest():
    """Triggers the ingestion process for documents in the docs/ folder."""
    try:
        stats = ingest_documents()
        return jsonify({"status": "success", "stats": stats}), 200
    except Exception as e:
        print(f"Error during ingestion: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/visitors/count', methods=['GET'])
def visitor_count():
    """Return visitor statistics."""
    try:
        counts = get_visitor_counts()
        return jsonify(counts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', os.environ.get('PORT', 5050)))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
