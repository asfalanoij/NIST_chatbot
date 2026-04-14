import json
import os
import pytest
from unittest.mock import patch


class TestHealthEndpoint:
    def test_health_returns_200(self, app_client):
        response = app_client.get("/api/health")
        assert response.status_code == 200

    def test_health_returns_healthy(self, app_client):
        response = app_client.get("/api/health")
        data = json.loads(response.data)
        assert data["status"] == "healthy"


class TestChatEndpoint:
    def test_chat_requires_message(self, app_client):
        response = app_client.post(
            "/api/chat",
            data=json.dumps({"message": ""}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_chat_returns_answer(self, app_client):
        response = app_client.post(
            "/api/chat",
            data=json.dumps({"message": "What is AC-2?"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "answer" in data
        assert "sources" in data

    def test_chat_returns_agent_info(self, app_client):
        response = app_client.post(
            "/api/chat",
            data=json.dumps({"message": "What is AC-2?"}),
            content_type="application/json",
        )
        data = json.loads(response.data)
        assert "agent_name" in data
        assert "agent_id" in data

    def test_chat_with_history(self, app_client):
        response = app_client.post(
            "/api/chat",
            data=json.dumps({
                "message": "Tell me more",
                "history": [
                    {"role": "user", "content": "What is AC-2?"},
                    {"role": "assistant", "content": "AC-2 is Account Management."},
                ],
            }),
            content_type="application/json",
        )
        assert response.status_code == 200

    def test_chat_missing_json(self, app_client):
        response = app_client.post(
            "/api/chat",
            data="not json",
            content_type="text/plain",
        )
        # Should return 400 or 500
        assert response.status_code in (400, 415, 500)


class TestApiKeyAuth:
    """Test X-API-Key authentication on protected endpoints."""

    def test_chat_no_key_when_api_key_not_configured(self, app_client):
        """When API_KEY env is empty, auth is disabled (dev mode)."""
        with patch.dict(os.environ, {"API_KEY": ""}, clear=False):
            response = app_client.post(
                "/api/chat",
                data=json.dumps({"message": "What is AC-2?"}),
                content_type="application/json",
            )
            assert response.status_code == 200

    def test_chat_rejected_without_key(self, app_client):
        """When API_KEY is set, requests without X-API-Key get 401."""
        with patch.dict(os.environ, {"API_KEY": "test-secret-key"}, clear=False):
            response = app_client.post(
                "/api/chat",
                data=json.dumps({"message": "What is AC-2?"}),
                content_type="application/json",
            )
            assert response.status_code == 401
            data = json.loads(response.data)
            assert "Unauthorized" in data["error"]

    def test_chat_rejected_with_wrong_key(self, app_client):
        """Wrong API key returns 401."""
        with patch.dict(os.environ, {"API_KEY": "test-secret-key"}, clear=False):
            response = app_client.post(
                "/api/chat",
                data=json.dumps({"message": "What is AC-2?"}),
                content_type="application/json",
                headers={"X-API-Key": "wrong-key"},
            )
            assert response.status_code == 401

    def test_chat_accepted_with_correct_key(self, app_client):
        """Correct API key passes auth."""
        with patch.dict(os.environ, {"API_KEY": "test-secret-key"}, clear=False):
            response = app_client.post(
                "/api/chat",
                data=json.dumps({"message": "What is AC-2?"}),
                content_type="application/json",
                headers={"X-API-Key": "test-secret-key"},
            )
            assert response.status_code == 200

    def test_health_not_protected(self, app_client):
        """Health endpoint is always accessible."""
        with patch.dict(os.environ, {"API_KEY": "test-secret-key"}, clear=False):
            response = app_client.get("/api/health")
            assert response.status_code == 200

    def test_visitors_not_protected(self, app_client):
        """Visitor count endpoint is always accessible."""
        with patch.dict(os.environ, {"API_KEY": "test-secret-key"}, clear=False):
            response = app_client.get("/api/visitors/count")
            assert response.status_code == 200


class TestStreamEndpoint:
    def test_stream_endpoint_exists(self, app_client):
        """POST /api/chat/stream returns 200 (not 404)."""
        response = app_client.post(
            "/api/chat/stream",
            data=json.dumps({"message": "What is AC-2?"}),
            content_type="application/json",
        )
        assert response.status_code == 200

    def test_stream_requires_api_key(self, app_client):
        """Stream endpoint respects X-API-Key auth."""
        with patch.dict(os.environ, {"API_KEY": "test-secret-key"}, clear=False):
            response = app_client.post(
                "/api/chat/stream",
                data=json.dumps({"message": "What is AC-2?"}),
                content_type="application/json",
            )
            assert response.status_code == 401

    def test_stream_returns_event_stream_content_type(self, app_client):
        """Stream endpoint responds with text/event-stream content type."""
        response = app_client.post(
            "/api/chat/stream",
            data=json.dumps({"message": "What is AC-2?"}),
            content_type="application/json",
        )
        assert "text/event-stream" in response.content_type


class TestSecurityHardening:
    def test_security_headers_present(self, app_client):
        """All responses must include X-Frame-Options and X-Content-Type-Options."""
        response = app_client.get("/api/health")
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_error_response_does_not_leak_exception(self, app_client):
        """500 error must return a generic message, not the exception string."""
        from unittest.mock import patch as _patch
        with _patch("api.chat.orchestrator") as mock_orch:
            mock_orch.route_and_chat.side_effect = RuntimeError(
                "/home/user/app/backend/agents.py line 42: secret_key=abc123"
            )
            response = app_client.post(
                "/api/chat",
                data=json.dumps({"message": "trigger error"}),
                content_type="application/json",
            )
        assert response.status_code == 500
        data = json.loads(response.data)
        assert "secret_key" not in data["error"]
        assert "agents.py" not in data["error"]
        assert data["error"] == "An internal error occurred. Please try again."

    def test_method_not_allowed_on_chat(self, app_client):
        """DELETE and GET on /api/chat must return 405."""
        assert app_client.delete("/api/chat").status_code == 405
        assert app_client.get("/api/chat").status_code == 405

    def test_oversized_message_rejected(self, app_client):
        """Messages > 2000 characters must be rejected with 400."""
        response = app_client.post(
            "/api/chat",
            data=json.dumps({"message": "A" * 2001}),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "too long" in data["error"].lower()

    def test_api_key_in_body_not_honoured(self, app_client):
        """API key provided in JSON body (not header) must be rejected."""
        with patch.dict(os.environ, {"API_KEY": "real-key"}, clear=False):
            response = app_client.post(
                "/api/chat",
                data=json.dumps({"message": "test", "api_key": "real-key"}),
                content_type="application/json",
            )
            assert response.status_code == 401

    def test_session_id_sanitised(self, app_client):
        """SQL injection fragment in X-Session-ID must not crash the app."""
        response = app_client.post(
            "/api/chat",
            data=json.dumps({"message": "What is AC-2?"}),
            content_type="application/json",
            headers={"X-Session-ID": "'; DROP TABLE interactions; --"},
        )
        # Must not be a 500 — either 200 (no auth) or 401 (auth enabled)
        assert response.status_code in (200, 401)
