import json
import logging
import os
import re
from flask import Blueprint, request, jsonify, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from agents import Orchestrator
from ingest import ingest_documents
from visitor_tracker import track_visit
from functools import wraps
import hmac

logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__)

# Initialize Orchestrator (singleton-like within the BP context if needed, but app.py should handle)
# Actually, it's better to pass it or have it accessible.
# For now, we'll create it here or assume it's attached to app.
orchestrator = Orchestrator()

_INTERNAL_ERROR_MSG = "An internal error occurred. Please try again."

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = os.environ.get("API_KEY")
        if not api_key:
            return f(*args, **kwargs)
        provided = request.headers.get("X-API-Key", "")
        if not provided or not hmac.compare_digest(provided, api_key):
            return jsonify({"error": "Unauthorized. Provide a valid X-API-Key header."}), 401
        return f(*args, **kwargs)
    return decorated

def _sanitise_session_id(raw: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\-_]', '', raw)[:64]

@chat_bp.before_request
def track_visitor():
    if request.path == "/api/chat" and request.method == "POST":
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ua = request.headers.get("User-Agent", "")
        track_visit(ip_address=ip, user_agent=ua, path=request.path)

@chat_bp.route('/chat', methods=['POST'])
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

@chat_bp.route('/chat/stream', methods=['POST'])
@require_api_key
def chat_stream():
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

@chat_bp.route('/ingest', methods=['POST'])
@require_api_key
def run_ingest():
    if os.environ.get("DISABLE_INGEST", "").lower() == "true":
        return jsonify({"error": "Ingestion is disabled in production."}), 403
    try:
        stats = ingest_documents()
        return jsonify({"status": "success", "stats": stats}), 200
    except Exception:
        logger.exception("Unhandled error in /api/ingest")
        return jsonify({"error": _INTERNAL_ERROR_MSG}), 500
