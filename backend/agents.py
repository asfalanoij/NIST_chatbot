import logging
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rag_engine import RAGEngine, get_llm

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Agent Personas — 7 Specialists (Pareto Optimum)
# Each solves a distinct compliance pain point for organizations.
# ---------------------------------------------------------------------

# Shared format rules injected into every agent prompt
_FORMAT_RULES = (
    "\n\nSTRICT FORMAT RULES (you MUST follow these):\n"
    "- Start with ONE bold summary sentence.\n"
    "- **Hierarchy**: Use nested bullets for details. E.g.,\n"
    "  - **Control**: Description\n"
    "    - Evidence: ...\n"
    "    - Test: ...\n"
    "- **Spacing**: Use blank lines between major points/bullets.\n"
    "- **Lists**: Use numbered lists (1., 2.) for sequential steps.\n"
    "- Bold control IDs: **AC-2**, **AC-2(1)**\n"
    "- Cite inline: [p.45]\n"
    "- Total response: MAX 200 words. Keep it concise but structured.\n"
    "- NEVER start with 'Okay' or 'Let's break down' — go straight to content.\n"
)

AGENTS = {
    "NIST_SPECIALIST": {
        "name": "NIST Controls Specialist",
        "prompt": (
            "You are a Senior NIST RMF & SP 800-53 Rev.5 Consultant. "
            "Reference Control IDs, enhancements, and RMF steps."
            + _FORMAT_RULES +
            "\nContext:\n{context}"
        ),
    },
    "AUDIT_SPECIALIST": {
        "name": "Audit & Assessment Specialist",
        "prompt": (
            "You are an Audit & Assessment Specialist (NIST SP 800-53A). "
            "List evidence artifacts, test procedures, and remediation steps."
            + _FORMAT_RULES +
            "\nContext:\n{context}"
        ),
    },
    "RISK_SPECIALIST": {
        "name": "Risk & Impact Specialist",
        "prompt": (
            "You are a Risk & FIPS 199/200 Specialist. "
            "Analyze CIA impact levels with concrete examples and tailoring guidance."
            + _FORMAT_RULES +
            "\nContext:\n{context}"
        ),
    },
    "COMPLIANCE_SPECIALIST": {
        "name": "Compliance Mapping Specialist",
        "prompt": (
            "You are a Compliance Mapping Specialist. "
            "Map NIST 800-53 to FedRAMP, CMMC, ISO 27001, SOC 2, HIPAA."
            + _FORMAT_RULES +
            "\nContext:\n{context}"
        ),
    },
    "PM_AGENT": {
        "name": "Product Manager Agent",
        "prompt": (
            "You are a PM & Strategic Advisor for NIST compliance. "
            "Frame compliance as business value, prioritize by effort-vs-impact."
            + _FORMAT_RULES +
            "\nContext:\n{context}"
        ),
    },
    "QA_AGENT": {
        "name": "QA & Test Strategy Specialist",
        "prompt": (
            "You are a QA & Test Strategy Specialist for NIST 800-53 compliance. "
            "Design test cases, validation criteria, test coverage matrices, "
            "and control testing methodology aligned with SP 800-53A."
            + _FORMAT_RULES +
            "\nContext:\n{context}"
        ),
    },
    "DEVSECOPS_AGENT": {
        "name": "DevSecOps & Pipeline Security Specialist",
        "prompt": (
            "You are a DevSecOps & Pipeline Security Specialist. "
            "Advise on CI/CD hardening, SAST/DAST integration, container security, "
            "infrastructure-as-code compliance, and shift-left security practices."
            + _FORMAT_RULES +
            "\nContext:\n{context}"
        ),
    },
}

# Route keywords for fast classification fallback
ROUTE_KEYWORDS = {
    "AUDIT_SPECIALIST": ["audit", "evidence", "artifact", "assessment", "poam", "ssp", "finding", "examine", "interview"],
    "RISK_SPECIALIST": ["risk", "impact", "fips", "threat", "vulnerability", "likelihood", "cia", "confidentiality", "integrity", "availability", "categorize"],
    "COMPLIANCE_SPECIALIST": ["fedramp", "cmmc", "iso", "soc", "hipaa", "mapping", "crosswalk", "compliance", "inherited", "authorization boundary", "continuous monitoring"],
    "PM_AGENT": ["roadmap", "prioritize", "priority", "stakeholder", "budget", "timeline", "phase", "milestone", "business case", "executive", "board", "quick win", "roi", "strategy", "plan"],
    "QA_AGENT": ["test case", "test plan", "test coverage", "validation", "regression", "acceptance test", "smoke test", "test strategy", "test automation", "qa", "quality assurance", "defect", "bug report"],
    "DEVSECOPS_AGENT": ["cicd", "ci/cd", "pipeline", "sast", "dast", "container security", "docker security", "kubernetes security", "infrastructure as code", "iac", "devsecops", "shift left", "code scanning", "dependency scanning", "supply chain"],
}

# ---------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------

class Orchestrator:
    def __init__(self):
        self.rag_engine = RAGEngine()
        self.router_llm = get_llm(temperature=0.0)
        self.valid_agents = list(AGENTS.keys())

        agent_descriptions = "\n".join(
            f"- {key}: {AGENTS[key]['name']}" for key in self.valid_agents
        )
        self.router_prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an intelligent router for a NIST Cybersecurity Chatbot. "
                "Classify the user's query into exactly one category:\n"
                f"{agent_descriptions}\n\n"
                "Return ONLY the category key (e.g., 'AUDIT_SPECIALIST'). No explanation."
            )),
            ("human", "{question}"),
        ])
        # Cache the router chain — no need to rebuild per request
        self._route_chain = self.router_prompt | self.router_llm | StrOutputParser()

    def _keyword_route(self, question: str) -> str:
        q_lower = question.lower()
        for agent_key, keywords in ROUTE_KEYWORDS.items():
            if any(kw in q_lower for kw in keywords):
                return agent_key
        return ""

    def route_and_chat(self, question: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        # 1. Route: keyword-first (saves an LLM call ~70% of the time)
        chosen_agent = self._keyword_route(question)

        if not chosen_agent:
            # No keyword match — use LLM router
            try:
                raw = self._route_chain.invoke({"question": question}).strip()
                matched = False
                for agent_key in self.valid_agents:
                    if agent_key in raw:
                        chosen_agent = agent_key
                        matched = True
                        break
                if not matched:
                    chosen_agent = "NIST_SPECIALIST"
            except Exception:
                chosen_agent = "NIST_SPECIALIST"

        agent_config = AGENTS[chosen_agent]
        logger.info("Routed -> %s", agent_config['name'])

        # 2. Execute RAG with the chosen persona
        response = self.rag_engine.chat(
            question=question,
            history=history,
            system_prompt_override=agent_config["prompt"],
        )

        response["agent_name"] = agent_config["name"]
        response["agent_id"] = chosen_agent
        return response
