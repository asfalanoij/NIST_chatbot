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
