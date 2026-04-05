import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents import AGENTS, ROUTE_KEYWORDS, Orchestrator


class TestAgentDefinitions:
    def test_four_agents_defined(self):
        assert len(AGENTS) == 4

    def test_all_agents_have_name_and_prompt(self):
        for key, agent in AGENTS.items():
            assert "name" in agent, f"{key} missing 'name'"
            assert "prompt" in agent, f"{key} missing 'prompt'"

    def test_all_agents_require_citations(self):
        for key, agent in AGENTS.items():
            assert "cite" in agent["prompt"].lower(), f"{key} prompt doesn't require citations"

    def test_expected_agent_keys(self):
        expected = {"NIST_SPECIALIST", "AUDIT_SPECIALIST", "RISK_SPECIALIST", "COMPLIANCE_SPECIALIST"}
        assert set(AGENTS.keys()) == expected

    def test_all_prompts_enforce_context_only(self):
        """Every agent prompt must include the grounding mandate."""
        for key, agent in AGENTS.items():
            prompt = agent["prompt"].lower()
            assert "only" in prompt and "context" in prompt, (
                f"{key} prompt missing 'ONLY from context' grounding mandate"
            )


class TestKeywordRouting:
    def test_audit_keywords(self):
        assert "audit" in ROUTE_KEYWORDS["AUDIT_SPECIALIST"]
        assert "evidence" in ROUTE_KEYWORDS["AUDIT_SPECIALIST"]

    def test_risk_keywords(self):
        assert "risk" in ROUTE_KEYWORDS["RISK_SPECIALIST"]
        assert "fips" in ROUTE_KEYWORDS["RISK_SPECIALIST"]

    def test_compliance_keywords(self):
        assert "fedramp" in ROUTE_KEYWORDS["COMPLIANCE_SPECIALIST"]


class TestOrchestratorRouting:
    @patch("agents.get_routing_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_audit(self, mock_rag, mock_get_routing_llm):
        mock_llm = MagicMock()
        mock_get_routing_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("I need audit evidence for my assessment")
        assert result == "AUDIT_SPECIALIST"

    @patch("agents.get_routing_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_risk(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("What is the risk impact of this vulnerability?")
        assert result == "RISK_SPECIALIST"

    @patch("agents.get_routing_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_default(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("What is AC-2?")
        assert result == ""  # no keyword match → empty, LLM router decides

    @patch("agents.get_routing_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_compliance(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("How do I map to fedramp?")
        assert result == "COMPLIANCE_SPECIALIST"

    @patch("agents.get_routing_llm")
    @patch("agents.RAGEngine")
    def test_removed_agents_fallback_to_default(self, mock_rag, mock_get_llm):
        """Queries that used to match PM/QA/DevSecOps should now return empty (default)."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        assert orch._keyword_route("Create a roadmap for our executive stakeholder") == ""
        assert orch._keyword_route("Create a test case with full test coverage") == ""
        assert orch._keyword_route("How to add SAST to CI/CD pipeline?") == ""


class TestRoutingLLM:
    def test_routing_llm_requires_gemini_key(self, monkeypatch):
        """get_routing_llm() raises EnvironmentError when GEMINI_API_KEY is absent."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        from rag_engine import get_routing_llm
        with pytest.raises(EnvironmentError, match="GEMINI_API_KEY"):
            get_routing_llm()

    def test_routing_llm_returns_gemini_when_key_set(self, monkeypatch):
        """get_routing_llm() returns a Gemini LLM when GEMINI_API_KEY is set."""
        monkeypatch.setenv("GEMINI_API_KEY", "fake-key-for-testing")
        mock_gemini_cls = MagicMock()
        mock_instance = MagicMock()
        mock_gemini_cls.return_value = mock_instance
        with patch("rag_engine.ChatGoogleGenerativeAI", mock_gemini_cls, create=True):
            # Need to re-import get_routing_llm to pick up the patch
            import importlib
            import rag_engine
            importlib.reload(rag_engine)
            result = rag_engine.get_routing_llm()
            assert result is not None

    @patch("agents.get_routing_llm")
    @patch("agents.RAGEngine")
    def test_orchestrator_uses_keyword_only_when_router_unavailable(self, mock_rag, mock_get_routing_llm):
        """Orchestrator sets _llm_router_available=False when get_routing_llm raises."""
        mock_get_routing_llm.side_effect = EnvironmentError("No key")
        orch = Orchestrator()
        assert orch._llm_router_available is False
        assert orch.router_llm is None
