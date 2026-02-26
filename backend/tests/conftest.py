import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Ensure backend is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def mock_ollama():
    """Mock Ollama LLM so tests don't need a running Ollama server."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="NIST_SPECIALIST")
    # Make it work with LangChain pipe operator
    mock_llm.__or__ = MagicMock(return_value=mock_llm)
    return mock_llm


@pytest.fixture
def app_client():
    """Create a Flask test client with mocked dependencies."""
    mock_orch_instance = MagicMock()
    mock_orch_instance.route_and_chat.return_value = {
        "answer": "Test answer about NIST controls.",
        "sources": [{"source": "nist_80053r5.pdf", "page": 42, "content_snippet": "AC-2..."}],
        "agent_name": "NIST Controls Specialist",
        "agent_id": "NIST_SPECIALIST",
    }

    # Patch Orchestrator class so reload creates our mock instance
    mock_orch_cls = MagicMock(return_value=mock_orch_instance)

    with patch.dict("sys.modules", {}):
        with patch("agents.Orchestrator", mock_orch_cls), \
             patch("agents.RAGEngine", MagicMock()), \
             patch("agents.get_llm", MagicMock()):
            import importlib
            import app as app_module
            importlib.reload(app_module)

            app_module.app.config["TESTING"] = True
            with app_module.app.test_client() as client:
                yield client
