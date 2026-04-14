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
    """Create a Flask test client with mocked dependencies.

    Patches Orchestrator at the blueprint module level (api.chat and
    api.health) so that no real LLM/embedding initialisation occurs.
    """
    mock_orch_instance = MagicMock()
    mock_orch_instance.route_and_chat.return_value = {
        "answer": "Test answer about NIST controls.",
        "sources": [{"source": "nist_80053r5.pdf", "page": 42, "content_snippet": "AC-2..."}],
        "agent_name": "NIST Controls Specialist",
        "agent_id": "NIST_SPECIALIST",
    }
    mock_orch_instance.route_and_chat_stream.return_value = iter([
        'data: {"type": "meta", "agent_name": "NIST Controls Specialist", "agent_id": "NIST_SPECIALIST"}\n\n',
        'data: {"chunk": "AC-2 is account management."}\n\n',
        "data: [DONE]\n\n",
    ])
    # For health check: rag_engine.index_path must be a real path for os.path.exists
    mock_orch_instance.rag_engine.index_path = os.path.join(
        os.path.dirname(__file__), ".."
    )

    mock_orch_cls = MagicMock(return_value=mock_orch_instance)

    with patch("agents.Orchestrator", mock_orch_cls), \
         patch("agents.RAGEngine", MagicMock()), \
         patch("agents.get_routing_llm", MagicMock()):
        import importlib
        import app as app_module
        importlib.reload(app_module)

        # Patch the orchestrator instances at the blueprint level
        import api.chat as chat_mod
        import api.health as health_mod
        original_chat_orch = chat_mod.orchestrator
        original_health_orch = health_mod.orchestrator
        chat_mod.orchestrator = mock_orch_instance
        health_mod.orchestrator = mock_orch_instance

        app_module.app.config["TESTING"] = True
        with app_module.app.test_client() as client:
            yield client

        # Restore originals
        chat_mod.orchestrator = original_chat_orch
        health_mod.orchestrator = original_health_orch
