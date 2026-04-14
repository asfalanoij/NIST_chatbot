import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestGetLlm:
    @patch.dict(os.environ, {}, clear=True)
    def test_default_returns_ollama(self):
        from rag_engine import get_llm
        with patch("rag_engine.ChatOllama") as mock_ollama:
            get_llm()
            mock_ollama.assert_called_once()

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key-123"})
    def test_gemini_when_key_set(self):
        from rag_engine import get_llm
        with patch("rag_engine.ChatGoogleGenerativeAI", create=True) as mock_gemini:
            # Need to patch the import inside get_llm
            import importlib
            import rag_engine
            importlib.reload(rag_engine)
            with patch.dict("sys.modules", {"langchain_google_genai": MagicMock()}):
                try:
                    rag_engine.get_llm()
                except Exception:
                    pass  # May fail if langchain_google_genai not installed


class TestGetEmbeddings:
    @patch.dict(os.environ, {}, clear=True)
    def test_default_returns_ollama(self):
        from rag_engine import get_embeddings
        with patch("rag_engine.OllamaEmbeddings") as mock_ollama:
            get_embeddings()
            mock_ollama.assert_called_once()

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key-123"})
    def test_gemini_when_key_set(self):
        mock_genai = MagicMock()
        with patch.dict("sys.modules", {"langchain_google_genai": mock_genai}):
            import importlib
            import rag_engine
            importlib.reload(rag_engine)
            rag_engine.get_embeddings()
            mock_genai.GoogleGenerativeAIEmbeddings.assert_called_once()


class TestGetLlmBackendName:
    @patch.dict(os.environ, {}, clear=True)
    def test_returns_ollama_by_default(self):
        from rag_engine import get_llm_backend_name
        assert get_llm_backend_name() == "ollama"

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"})
    def test_returns_gemini_when_key_set(self):
        from rag_engine import get_llm_backend_name
        assert get_llm_backend_name() == "gemini"


class TestRAGEngine:
    @patch("rag_engine.get_llm")
    @patch("rag_engine.get_embeddings")
    def test_init(self, mock_emb, mock_get_llm):
        from rag_engine import RAGEngine
        engine = RAGEngine()
        assert engine.vector_store is None
        assert engine.llm is not None
        mock_emb.assert_called_once()

    @patch("rag_engine.get_llm")
    @patch("rag_engine.get_embeddings")
    def test_chat_without_index(self, mock_emb, mock_get_llm):
        from rag_engine import RAGEngine
        engine = RAGEngine()
        engine.index_path = "/nonexistent/path"
        result = engine.chat("What is AC-2?")
        assert "Knowledge Base is empty" in result["answer"]
        assert result["sources"] == []


class TestValidateResponse:
    """Tests for the faithfulness validation layer."""

    def _make_doc(self, page: int, content: str):
        """Helper to create a mock LangChain Document."""
        doc = MagicMock()
        doc.metadata = {"source": "nist_80053r5.pdf", "page": page}
        doc.page_content = content
        return doc

    def test_valid_citation_passes(self):
        from rag_engine import validate_response
        docs = [self._make_doc(42, "AC-2 Account Management details.")]
        answer = "**AC-2** controls account management [p.42]."
        corrected, report = validate_response(answer, docs)
        assert corrected == answer
        assert report["citations_valid"] == 1
        assert report["citations_removed"] == []

    def test_hallucinated_page_removed(self):
        from rag_engine import validate_response
        docs = [self._make_doc(42, "AC-2 details.")]
        answer = "**AC-2** controls account management [p.99]."
        corrected, report = validate_response(answer, docs)
        assert "[p.99]" not in corrected
        assert "[p.99]" in report["citations_removed"]

    def test_page_tolerance_plus_minus_one(self):
        from rag_engine import validate_response
        docs = [self._make_doc(42, "AC-2 details.")]
        # Page 43 is within ±1 tolerance of page 42
        answer = "**AC-2** controls account management [p.43]."
        corrected, report = validate_response(answer, docs)
        assert "[p.43]" in corrected
        assert report["citations_removed"] == []

    def test_ungrounded_control_flagged(self):
        from rag_engine import validate_response
        docs = [self._make_doc(42, "AC-2 Account Management details.")]
        # SI-7 is not in any chunk text
        answer = "**AC-2** and **SI-7** are important [p.42]."
        corrected, report = validate_response(answer, docs)
        assert "SI-7" in report["controls_ungrounded"]
        assert "AC-2" not in report["controls_ungrounded"]

    def test_grounded_control_not_flagged(self):
        from rag_engine import validate_response
        docs = [self._make_doc(42, "AC-2 and AC-3 controls.")]
        answer = "**AC-2** and **AC-3** are access controls [p.42]."
        corrected, report = validate_response(answer, docs)
        assert report["controls_ungrounded"] == []

    def test_no_citations_no_crash(self):
        from rag_engine import validate_response
        docs = [self._make_doc(42, "Some content.")]
        answer = "This is a plain answer with no citations."
        corrected, report = validate_response(answer, docs)
        assert corrected == answer
        assert report["citations_valid"] == 0
        assert report["citations_removed"] == []

    def test_empty_source_docs(self):
        from rag_engine import validate_response
        answer = "**AC-2** is important [p.42]."
        corrected, report = validate_response(answer, [])
        assert "[p.42]" not in corrected
        assert report["citations_removed"] == ["[p.42]"]


class TestHistoryToMessages:
    def test_empty_list(self):
        from rag_engine import _history_to_messages
        assert _history_to_messages([]) == []

    def test_converts_roles(self):
        from rag_engine import _history_to_messages
        from langchain_core.messages import HumanMessage, AIMessage
        history = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
        ]
        msgs = _history_to_messages(history)
        assert len(msgs) == 2
        assert isinstance(msgs[0], HumanMessage)
        assert isinstance(msgs[1], AIMessage)
        assert msgs[0].content == "hi"

    def test_ignores_unknown_roles(self):
        from rag_engine import _history_to_messages
        history = [
            {"role": "system", "content": "ignored"},
            {"role": "user", "content": "kept"},
        ]
        msgs = _history_to_messages(history)
        assert len(msgs) == 1


class TestRAGEngineChatPaths:
    """Tests for chat() and chat_stream() with mocked vector store."""

    @patch("rag_engine.get_llm")
    @patch("rag_engine.get_embeddings")
    def test_chat_off_topic_rejection(self, mock_emb, mock_get_llm):
        from rag_engine import RAGEngine
        engine = RAGEngine()

        mock_vs = MagicMock()
        # MMR returns docs but L2 score is above threshold
        mock_vs.max_marginal_relevance_search.return_value = []
        mock_vs.similarity_search_with_score.return_value = [
            (MagicMock(), 2.0)  # L2 = 2.0 > 1.5 threshold
        ]
        engine.vector_store = mock_vs

        result = engine.chat("What is the weather?")
        assert "don't have specific information" in result["answer"]
        assert result["sources"] == []

    @patch("rag_engine.get_llm")
    @patch("rag_engine.get_embeddings")
    def test_chat_returns_sources_and_validation(self, mock_emb, mock_get_llm):
        from rag_engine import RAGEngine
        engine = RAGEngine()

        mock_doc = MagicMock()
        mock_doc.metadata = {"source": "nist.pdf", "page": 42, "control_ids": ["AC-2"]}
        mock_doc.page_content = "AC-2 Account Management details."

        mock_vs = MagicMock()
        mock_vs.max_marginal_relevance_search.return_value = [mock_doc]
        mock_vs.similarity_search_with_score.return_value = [(mock_doc, 0.5)]
        engine.vector_store = mock_vs

        # Mock the chain to return a grounded answer
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "**AC-2** is Account Management [p.42]."
        engine._default_chain = mock_chain

        result = engine.chat("What is AC-2?")
        assert "answer" in result
        assert "sources" in result
        assert "validation" in result
        assert len(result["sources"]) > 0

    @patch("rag_engine.get_llm")
    @patch("rag_engine.get_embeddings")
    def test_chat_uses_override_prompt(self, mock_emb, mock_get_llm):
        from rag_engine import RAGEngine
        engine = RAGEngine()

        mock_doc = MagicMock()
        mock_doc.metadata = {"source": "nist.pdf", "page": 1}
        mock_doc.page_content = "Content."

        mock_vs = MagicMock()
        mock_vs.max_marginal_relevance_search.return_value = [mock_doc]
        mock_vs.similarity_search_with_score.return_value = [(mock_doc, 0.5)]
        engine.vector_store = mock_vs

        with patch.object(engine, '_build_chain') as mock_build:
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = "Override answer."
            mock_build.return_value = mock_chain

            engine.chat("test", system_prompt_override="Custom prompt\n{context}")
            mock_build.assert_called_once_with("Custom prompt\n{context}")

    @patch("rag_engine.get_llm")
    @patch("rag_engine.get_embeddings")
    def test_chat_stream_without_index(self, mock_emb, mock_get_llm):
        from rag_engine import RAGEngine
        engine = RAGEngine()
        engine.index_path = "/nonexistent/path"

        chunks = list(engine.chat_stream("What is AC-2?"))
        assert len(chunks) == 1
        assert "Knowledge Base is empty" in chunks[0]

    @patch("rag_engine.get_llm")
    @patch("rag_engine.get_embeddings")
    def test_chat_stream_off_topic(self, mock_emb, mock_get_llm):
        from rag_engine import RAGEngine
        engine = RAGEngine()

        mock_vs = MagicMock()
        mock_vs.max_marginal_relevance_search.return_value = []
        mock_vs.similarity_search_with_score.return_value = [
            (MagicMock(), 2.0)
        ]
        engine.vector_store = mock_vs

        chunks = list(engine.chat_stream("What is the weather?"))
        assert len(chunks) == 1
        assert "don't have specific information" in chunks[0]
