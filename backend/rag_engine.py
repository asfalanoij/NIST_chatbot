import os
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


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


def get_llm_backend_name():
    """Return which LLM backend is active."""
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    return "ollama"


class RAGEngine:
    def __init__(self):
        self.index_path = os.path.join(os.path.dirname(__file__), "index_kms")
        self.embeddings = get_embeddings()
        self.vector_store = None
        self.llm = get_llm(temperature=0.2)

        self.default_system_prompt = (
            "You are a concise NIST 800-53 consultant. You MUST follow these rules:\n\n"
            "FORMAT: Use markdown. Start with a bold one-line summary.\n"
            "HIERARCHY: Use nested bullets. Main point -> Sub-point.\n"
            "SPACING: Add blank lines between main bullet points.\n"
            "LENGTH: Maximum 150 words total.\n"
            "STYLE: No filler, no intros, no 'Okay let's...', no conclusions. Just facts.\n"
            "CITATIONS: Inline as [p.XX].\n"
            "CONTROLS: Bold IDs like **AC-2**, **AC-2(1)**.\n\n"
            "Context:\n{context}"
        )

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

        # Single retrieval pass — fixes the double-call bug
        source_docs = vs.similarity_search(question, k=5)

        # Format context from retrieved docs
        context_text = "\n\n---\n\n".join(
            f"[{doc.metadata.get('source', 'Unknown')} p.{doc.metadata.get('page', '?')}]\n{doc.page_content}"
            for doc in source_docs
        )

        # Build prompt
        system_prompt = system_prompt_override or self.default_system_prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}"),
        ])

        # Execute chain
        chain = prompt | self.llm | StrOutputParser()
        answer = chain.invoke({"context": context_text, "question": question})

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

        return {"answer": answer, "sources": sources}
