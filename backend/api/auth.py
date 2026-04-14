import hmac
import os
from functools import wraps
from flask import jsonify, request


def require_api_key(f):
    """Reject requests when API_KEY is set and no valid X-API-Key header is provided.

    When API_KEY env var is empty (dev mode), the decorator is a no-op.
    """
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
