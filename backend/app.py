import os
import logging
from flask import Flask, jsonify, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Import Blueprints
from api.chat import chat_bp
from api.config import config_bp
from api.crossmap import crossmap_bp
from api.health import health_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Reject bodies larger than 16 KB
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

    # CORS: use env var or default to localhost dev origins
    cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:5050,http://127.0.0.1:5173,http://127.0.0.1:5050")
    CORS(app, origins=[o.strip() for o in cors_origins.split(",")])

    # Flask config from env
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")

    # Rate limiting
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )

    # Security Headers
    @app.after_request
    def set_security_headers(response: Response) -> Response:
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        if not app.debug:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    # Error Handlers
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({"error": "Rate limit exceeded. Please try again later.", "retry_after": e.description}), 429

    @app.errorhandler(413)
    def payload_too_large(e):
        return jsonify({"error": "Request payload too large."}), 413

    # Register Blueprints
    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(config_bp, url_prefix="/api")
    app.register_blueprint(crossmap_bp, url_prefix="/api/crossmap")
    app.register_blueprint(health_bp, url_prefix="/api")

    return app

app = create_app()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    port = int(os.environ.get('FLASK_PORT', os.environ.get('PORT', 5050)))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
