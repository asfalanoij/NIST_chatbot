import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents import AGENTS, ROUTE_KEYWORDS, Orchestrator


class TestAgentDefinitions:
    def test_seven_agents_defined(self):
        assert len(AGENTS) == 7

    def test_all_agents_have_name_and_prompt(self):
        for key, agent in AGENTS.items():
            assert "name" in agent, f"{key} missing 'name'"
            assert "prompt" in agent, f"{key} missing 'prompt'"

    def test_all_agents_require_citations(self):
        for key, agent in AGENTS.items():
            assert "cite" in agent["prompt"].lower(), f"{key} prompt doesn't require citations"

    def test_expected_agent_keys(self):
        expected = {"NIST_SPECIALIST", "AUDIT_SPECIALIST", "RISK_SPECIALIST", "COMPLIANCE_SPECIALIST", "PM_AGENT", "QA_AGENT", "DEVSECOPS_AGENT"}
        assert set(AGENTS.keys()) == expected


class TestKeywordRouting:
    def test_audit_keywords(self):
        assert "audit" in ROUTE_KEYWORDS["AUDIT_SPECIALIST"]
        assert "evidence" in ROUTE_KEYWORDS["AUDIT_SPECIALIST"]

    def test_risk_keywords(self):
        assert "risk" in ROUTE_KEYWORDS["RISK_SPECIALIST"]
        assert "fips" in ROUTE_KEYWORDS["RISK_SPECIALIST"]

    def test_compliance_keywords(self):
        assert "fedramp" in ROUTE_KEYWORDS["COMPLIANCE_SPECIALIST"]

    def test_pm_keywords(self):
        assert "roadmap" in ROUTE_KEYWORDS["PM_AGENT"]

    def test_qa_keywords(self):
        assert "test case" in ROUTE_KEYWORDS["QA_AGENT"]
        assert "validation" in ROUTE_KEYWORDS["QA_AGENT"]

    def test_devsecops_keywords(self):
        assert "pipeline" in ROUTE_KEYWORDS["DEVSECOPS_AGENT"]
        assert "sast" in ROUTE_KEYWORDS["DEVSECOPS_AGENT"]


class TestOrchestratorRouting:
    @patch("agents.get_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_audit(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("I need audit evidence for my assessment")
        assert result == "AUDIT_SPECIALIST"

    @patch("agents.get_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_risk(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("What is the risk impact of this vulnerability?")
        assert result == "RISK_SPECIALIST"

    @patch("agents.get_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_default(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("What is AC-2?")
        assert result == ""  # no keyword match → empty, LLM router decides

    @patch("agents.get_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_pm(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("Create a roadmap for our executive stakeholder")
        assert result == "PM_AGENT"

    @patch("agents.get_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_compliance(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("How do I map to fedramp?")
        assert result == "COMPLIANCE_SPECIALIST"

    @patch("agents.get_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_qa(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("Create a test case with full test coverage for validation")
        assert result == "QA_AGENT"

    @patch("agents.get_llm")
    @patch("agents.RAGEngine")
    def test_keyword_fallback_devsecops(self, mock_rag, mock_get_llm):
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm
        orch = Orchestrator()
        result = orch._keyword_route("How to add SAST to CI/CD pipeline?")
        assert result == "DEVSECOPS_AGENT"
