import json
import logging
import time
import os
from typing import Dict, Any, List, Generator
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rag_engine import RAGEngine, get_routing_llm, validate_response
from cache import LRUCache
from interaction_log import log_interaction

logger = logging.getLogger(__name__)

# Path to the SSoT JSON file
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
AGENTS_PATH = os.path.join(DATA_DIR, "agents.json")

def load_agents_config() -> Dict[str, Any]:
    """Load agent definitions and routing keywords from JSON."""
    try:
        with open(AGENTS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error("Failed to load agents config: %s", e)
        return {}

AGENTS_CONFIG = load_agents_config()

# Derived mappings for backward compatibility or efficient access
AGENTS = {k: {"name": v["name"], "prompt": v["prompt"]} for k, v in AGENTS_CONFIG.items()}
ROUTE_KEYWORDS = {k: v["keywords"] for k, v in AGENTS_CONFIG.items() if v.get("keywords")}

# ---------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------

class Orchestrator:
    def __init__(self):
        self.rag_engine = RAGEngine()
        self.cache = LRUCache(maxsize=128, ttl_seconds=3600)
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

        # Always use Gemini Flash for routing — avoids ChatOllama cold-start (~3s).
        # If GEMINI_API_KEY is absent, fall back to keyword-only routing.
        self._llm_router_available = False
        try:
            self.router_llm = get_routing_llm()
            self._route_chain = self.router_prompt | self.router_llm | StrOutputParser()
            self._llm_router_available = True
        except EnvironmentError as exc:
            logger.warning("LLM router unavailable (%s). Using keyword-only routing.", exc)
            self.router_llm = None
            self._route_chain = None

    def _keyword_route(self, question: str) -> str:
        q_lower = question.lower()
        for agent_key, keywords in ROUTE_KEYWORDS.items():
            if any(kw in q_lower for kw in keywords):
                return agent_key
        return ""

    def route_and_chat(
        self,
        question: str,
        history: List[Dict[str, str]] = None,
        session_id: str = "",
    ) -> Dict[str, Any]:
        start_ms = int(time.time() * 1000)

        # 1. Route: keyword-first (saves an LLM call ~70% of the time)
        chosen_agent = self._keyword_route(question)

        if not chosen_agent:
            # No keyword match — use LLM router if available, else default
            if self._llm_router_available:
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
            else:
                chosen_agent = "NIST_SPECIALIST"

        agent_config = AGENTS[chosen_agent]
        logger.info("Routed -> %s", agent_config['name'])

        # 2. Cache check — only for stateless queries (no history)
        is_stateless = not history
        if is_stateless:
            cached = self.cache.get(question, chosen_agent)
            if cached is not None:
                latency_ms = int(time.time() * 1000) - start_ms
                log_interaction(
                    question=question,
                    answer=cached.get("answer", ""),
                    latency_ms=latency_ms,
                    session_id=session_id,
                    agent_id=chosen_agent,
                    agent_name=agent_config["name"],
                    sources=cached.get("sources", []),
                    cached=True,
                )
                return cached

        # 3. Execute RAG with the chosen persona
        response = self.rag_engine.chat(
            question=question,
            history=history,
            system_prompt_override=agent_config["prompt"],
        )

        response["agent_name"] = agent_config["name"]
        response["agent_id"] = chosen_agent

        # 4. Store in cache (stateless only)
        if is_stateless:
            self.cache.set(question, chosen_agent, response)

        # 5. Log interaction
        latency_ms = int(time.time() * 1000) - start_ms
        log_interaction(
            question=question,
            answer=response.get("answer", ""),
            latency_ms=latency_ms,
            session_id=session_id,
            agent_id=chosen_agent,
            agent_name=agent_config["name"],
            sources=response.get("sources", []),
            cached=False,
            validation=response.get("validation"),
        )

        return response

    def route_and_chat_stream(
        self,
        question: str,
        history: List[Dict[str, str]] = None,
        session_id: str = "",
    ) -> Generator[str, None, None]:
        """Yield SSE-formatted lines for the streaming endpoint.

        Sequence:
          data: {"type": "meta", "agent_name": "...", "agent_id": "..."}
          data: {"chunk": "..."}  (× N)
          data: [DONE]
        """
        start_ms = int(time.time() * 1000)

        chosen_agent = self._keyword_route(question)
        if not chosen_agent:
            if self._llm_router_available:
                try:
                    raw = self._route_chain.invoke({"question": question}).strip()
                    for agent_key in self.valid_agents:
                        if agent_key in raw:
                            chosen_agent = agent_key
                            break
                    if not chosen_agent:
                        chosen_agent = "NIST_SPECIALIST"
                except Exception:
                    chosen_agent = "NIST_SPECIALIST"
            else:
                chosen_agent = "NIST_SPECIALIST"

        agent_config = AGENTS[chosen_agent]
        logger.info("Stream routed -> %s", agent_config["name"])

        yield f"data: {json.dumps({'type': 'meta', 'agent_name': agent_config['name'], 'agent_id': chosen_agent})}\n\n"

        accumulated: list[str] = []
        for chunk in self.rag_engine.chat_stream(
            question=question,
            history=history,
            system_prompt_override=agent_config["prompt"],
        ):
            accumulated.append(chunk)
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        yield "data: [DONE]\n\n"

        # Validate after stream completes
        full_answer = "".join(accumulated)
        source_docs = getattr(self.rag_engine, "last_source_docs", [])
        _, validation = validate_response(full_answer, source_docs)

        # Log after stream completes
        latency_ms = int(time.time() * 1000) - start_ms
        log_interaction(
            question=question,
            answer=full_answer,
            latency_ms=latency_ms,
            session_id=session_id,
            agent_id=chosen_agent,
            agent_name=agent_config["name"],
            cached=False,
            validation=validation,
        )
