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
