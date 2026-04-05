import logging
import os
import re
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

logger = logging.getLogger(__name__)

# L2 distance threshold — chunks above this are considered off-topic.
# FAISS L2: 0 = identical, ~1.0 = related, >1.5 = likely irrelevant.
RELEVANCE_THRESHOLD = 1.5

# Faithfulness validation patterns
_CITATION_RE = re.compile(r'\[p\.(\d+)\]')
_CONTROL_ID_RE = re.compile(r'\*\*([A-Z]{2}-\d+(?:\(\d+\))?)\*\*')


def get_llm(temperature=0.2):
    """Return Gemini LLM if API key is set, otherwise fall back to Ollama."""
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
            google_api_key=gemini_key,
            temperature=temperature,
        )
    return ChatOllama(
        model=os.environ.get("OLLAMA_MODEL", "llama3"),
        temperature=temperature,
    )


def get_embeddings():
    """Return Gemini embeddings if API key is set, otherwise fall back to Ollama."""
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(
            model=os.environ.get("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001"),
            google_api_key=gemini_key,
        )
    return OllamaEmbeddings(
        model=os.environ.get("OLLAMA_MODEL", "llama3"),
    )


def get_routing_llm():
    """Return Gemini Flash for routing (temperature=0).

    Always uses Gemini — avoids ChatOllama cold-start (~3s if Ollama not running).
    Raises EnvironmentError if GEMINI_API_KEY is absent so callers can fall back
    to keyword-only routing without crashing.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        raise EnvironmentError(
            "GEMINI_API_KEY is required for LLM routing. "
            "Falling back to keyword-only routing."
        )
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_key,
        temperature=0.0,
    )


def get_llm_backend_name():
    """Return which LLM backend is active."""
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    return "ollama"


def _history_to_messages(history: List[Dict[str, str]]):
    """Convert chat history dicts to LangChain message objects."""
    messages = []
    for entry in history:
        role = entry.get("role", "")
        content = entry.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
    return messages


def validate_response(
    answer: str,
    source_docs: list,
) -> tuple[str, dict]:
    """Verify citations and control IDs against retrieved chunks.

    Returns (corrected_answer, validation_report).
    - Strips [p.XX] citations where XX is not in any retrieved chunk's page metadata (±1 tolerance).
    - Flags bolded control IDs not found in any retrieved chunk text.
    """
    # Build valid page set from retrieved docs (±1 tolerance for chunk overlap)
    raw_pages: set[int] = set()
    for doc in source_docs:
        page = doc.metadata.get("page")
        if page is not None:
            try:
                raw_pages.add(int(page))
            except (ValueError, TypeError):
                pass
    valid_pages: set[int] = set()
    for p in raw_pages:
        valid_pages.update([p - 1, p, p + 1])

    # Build control ID set from metadata (preferred) or text fallback
    metadata_control_ids: set[str] = set()
    for doc in source_docs:
        ids = doc.metadata.get("control_ids", [])
        if ids:
            metadata_control_ids.update(ids)
    # Fallback: concatenate text for substring check if no metadata
    chunk_text = " ".join(doc.page_content for doc in source_docs)

    # Check 1: Citation verification
    citations_removed: list[str] = []
    def _check_citation(match: re.Match) -> str:
        page_num = int(match.group(1))
        if page_num in valid_pages:
            return match.group(0)
        citations_removed.append(match.group(0))
        return ""  # strip invalid citation

    corrected = _CITATION_RE.sub(_check_citation, answer)

    # Check 2: Control ID verification (use metadata if available, else text)
    controls_ungrounded: list[str] = []
    for match in _CONTROL_ID_RE.finditer(corrected):
        control_id = match.group(1)
        if metadata_control_ids:
            if control_id not in metadata_control_ids:
                controls_ungrounded.append(control_id)
        elif control_id not in chunk_text:
            controls_ungrounded.append(control_id)

    # Count valid citations remaining
    citations_valid = len(_CITATION_RE.findall(corrected))

    report = {
        "citations_valid": citations_valid,
        "citations_removed": citations_removed,
        "controls_ungrounded": controls_ungrounded,
    }

    if citations_removed or controls_ungrounded:
        logger.warning(
            "Faithfulness check: removed=%s, ungrounded=%s",
            citations_removed, controls_ungrounded,
        )

    return corrected, report


class RAGEngine:
    def __init__(self):
        self.index_path = os.path.join(os.path.dirname(__file__), "index_kms")
        self.embeddings = get_embeddings()
        self.vector_store = None
        self.llm = get_llm(temperature=0.2)

        self.default_system_prompt = (
            "You are a NIST 800-53 Rev.5 reference assistant. "
            "You answer ONLY from the provided context.\n\n"
            "RULES:\n"
            "1. ONLY state facts that appear in the Context below. "
            "Never add information from your training data.\n"
            "2. If the context does not contain the answer, say: "
            '"This information is not covered in the retrieved NIST 800-53 sections."\n'
            "3. Every claim MUST cite [p.XX] matching a page number "
            "from the context headers.\n"
            "4. Do NOT invent page numbers. Only cite pages shown in "
            "context headers.\n"
            "5. Bold all control IDs: **AC-2**, **SC-7(1)**.\n"
            "6. Markdown with nested bullets. Start with a bold one-line summary.\n"
            "7. Maximum 200 words. No filler, no introductions, no conclusions.\n\n"
            "Context:\n{context}"
        )

        # Cache the default chain (rebuilt only when system_prompt_override is given)
        self._default_chain = self._build_chain(self.default_system_prompt)

    def _build_chain(self, system_prompt: str):
        """Build a prompt | llm | parser chain with history support."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{question}"),
        ])
        return prompt | self.llm | StrOutputParser()

    def _load_vector_store(self):
        if self.vector_store is None:
            if os.path.exists(self.index_path):
                self.vector_store = FAISS.load_local(
                    self.index_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
            else:
                raise FileNotFoundError("Vector index not found. Run ingestion first (make ingest).")
        return self.vector_store

    def chat(
        self,
        question: str,
        history: Optional[List[Dict[str, str]]] = None,
        system_prompt_override: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            vs = self._load_vector_store()
        except FileNotFoundError:
            return {
                "answer": "The Knowledge Base is empty. Please upload NIST documents to docs/ and run ingestion.",
                "sources": [],
            }

        # MMR retrieval — diversifies results across different pages/sections
        source_docs = vs.max_marginal_relevance_search(question, k=5, fetch_k=20)

        # Score threshold guard — reject off-topic queries
        scored = vs.similarity_search_with_score(question, k=1)
        if scored and scored[0][1] > RELEVANCE_THRESHOLD:
            logger.info("Off-topic query (L2=%.2f): %s", scored[0][1], question[:80])
            return {
                "answer": "I don't have specific information on that topic in the NIST 800-53 knowledge base. Please ask about NIST security controls, compliance, or risk management.",
                "sources": [],
            }

        # Format context from retrieved docs
        context_text = "\n\n---\n\n".join(
            f"[{doc.metadata.get('source', 'Unknown')} p.{doc.metadata.get('page', '?')}]\n{doc.page_content}"
            for doc in source_docs
        )

        # Select chain: cached default or build new for override
        if system_prompt_override:
            chain = self._build_chain(system_prompt_override)
        else:
            chain = self._default_chain

        # Convert history to LangChain messages
        chat_history = _history_to_messages(history) if history else []

        answer = chain.invoke({
            "context": context_text,
            "question": question,
            "chat_history": chat_history,
        })

        # Faithfulness validation — strip hallucinated citations / flag ungrounded controls
        answer, validation = validate_response(answer, source_docs)

        # Build source citations
        sources = []
        seen = set()
        for doc in source_docs:
            key = (doc.metadata.get("source", ""), doc.metadata.get("page", ""))
            if key not in seen:
                seen.add(key)
                sources.append({
                    "source": doc.metadata.get("source", "Unknown"),
                    "page": doc.metadata.get("page", "Unknown"),
                    "content_snippet": doc.page_content[:200] + "...",
                })

        return {"answer": answer, "sources": sources, "validation": validation}

    def chat_stream(
        self,
        question: str,
        history: Optional[List[Dict[str, str]]] = None,
        system_prompt_override: Optional[str] = None,
    ):
        """Yield answer chunks as strings.

        Callers should accumulate chunks into a full answer for logging/caching.
        After iteration completes, ``self.last_source_docs`` holds the retrieved
        documents for post-stream faithfulness validation.
        """
        self.last_source_docs = []
        try:
            vs = self._load_vector_store()
        except FileNotFoundError:
            yield "The Knowledge Base is empty. Please upload NIST documents and run ingestion."
            return

        source_docs = vs.max_marginal_relevance_search(question, k=5, fetch_k=20)
        self.last_source_docs = source_docs

        scored = vs.similarity_search_with_score(question, k=1)
        if scored and scored[0][1] > RELEVANCE_THRESHOLD:
            logger.info("Off-topic query (L2=%.2f): %s", scored[0][1], question[:80])
            yield "I don't have specific information on that topic in the NIST 800-53 knowledge base. Please ask about NIST security controls, compliance, or risk management."
            return

        context_text = "\n\n---\n\n".join(
            f"[{doc.metadata.get('source', 'Unknown')} p.{doc.metadata.get('page', '?')}]\n{doc.page_content}"
            for doc in source_docs
        )

        chain = self._build_chain(system_prompt_override) if system_prompt_override else self._default_chain
        chat_history = _history_to_messages(history) if history else []

        for chunk in chain.stream({"context": context_text, "question": question, "chat_history": chat_history}):
            yield chunk
