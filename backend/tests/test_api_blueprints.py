import json
import os
import sys
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestConfigEndpoints:
    def test_config_agents_returns_list(self, app_client):
        response = app_client.get("/api/config/agents")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 4

    def test_config_agents_has_required_keys(self, app_client):
        response = app_client.get("/api/config/agents")
        data = json.loads(response.data)
        required_keys = {"id", "name", "description", "icon", "details"}
        for agent in data:
            assert required_keys.issubset(agent.keys()), f"Missing keys in {agent.get('id')}"

    def test_config_crossmap_returns_json(self, app_client):
        response = app_client.get("/api/config/crossmap")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)


class TestHealthDetails:
    def test_health_returns_checks_object(self, app_client):
        response = app_client.get("/api/health")
        data = json.loads(response.data)
        assert "checks" in data
        assert "database" in data["checks"]
        assert "faiss_index" in data["checks"]

    def test_visitors_count_returns_counts(self, app_client):
        response = app_client.get("/api/visitors/count")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "unique_visitors" in data
        assert "total_visits" in data


class TestInteractionsStats:
    def test_requires_auth(self, app_client):
        with patch.dict(os.environ, {"API_KEY": "secret-key"}, clear=False):
            response = app_client.get("/api/interactions/stats")
            assert response.status_code == 401

    def test_returns_data_with_auth(self, app_client):
        with patch.dict(os.environ, {"API_KEY": ""}, clear=False):
            response = app_client.get("/api/interactions/stats")
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "total_interactions" in data


class TestIngestEndpoint:
    def test_disabled_in_prod(self, app_client):
        with patch.dict(os.environ, {"DISABLE_INGEST": "true"}, clear=False):
            response = app_client.post("/api/ingest")
            assert response.status_code == 403


class TestStreamEdgeCases:
    def test_missing_message_returns_400(self, app_client):
        response = app_client.post(
            "/api/chat/stream",
            data=json.dumps({"message": ""}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_oversized_message_returns_400(self, app_client):
        response = app_client.post(
            "/api/chat/stream",
            data=json.dumps({"message": "A" * 2001}),
            content_type="application/json",
        )
        assert response.status_code == 400
