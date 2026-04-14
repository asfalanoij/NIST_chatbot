import os
import logging
from flask import Blueprint, jsonify
from visitor_tracker import get_visitor_counts, check_db_health
from interaction_log import get_stats as get_interaction_stats
from agents import Orchestrator
from api.auth import require_api_key

logger = logging.getLogger(__name__)

health_bp = Blueprint("health", __name__)

orchestrator = Orchestrator()

_INTERNAL_ERROR_MSG = "An internal error occurred. Please try again."

@health_bp.route('/health', methods=['GET'])
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

@health_bp.route('/visitors/count', methods=['GET'])
def visitor_count():
    """Return visitor statistics."""
    try:
        counts = get_visitor_counts()
        return jsonify(counts), 200
    except Exception:
        logger.exception("Unhandled error in /api/visitors/count")
        return jsonify({"error": _INTERNAL_ERROR_MSG}), 500

@health_bp.route('/interactions/stats', methods=['GET'])
@require_api_key
def interaction_stats():
    """Return aggregate interaction quality stats (admin only)."""
    try:
        stats = get_interaction_stats()
        return jsonify(stats), 200
    except Exception:
        logger.exception("Unhandled error in /api/interactions/stats")
        return jsonify({"error": _INTERNAL_ERROR_MSG}), 500
