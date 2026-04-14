import sys
import os
import re
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestControlRegex:
    """Test the NIST control ID regex used during ingestion.

    Note: _CONTROL_RE uses a capture group around the family prefix,
    so findall() returns family prefixes like ['AC', 'SI'].
    Full match strings require finditer() + match.group(0).
    """

    def test_extracts_nist_ids(self):
        from ingest import _CONTROL_RE
        text = "AC-2 Account Management, SI-7 Software Integrity, SC-28 Protection at Rest"
        full_matches = [m.group(0) for m in _CONTROL_RE.finditer(text)]
        assert "AC-2" in full_matches
        assert "SI-7" in full_matches
        assert "SC-28" in full_matches

    def test_rejects_invalid_families(self):
        from ingest import _CONTROL_RE
        text = "XX-99 is not a real control. ZZ-1 either."
        matches = list(_CONTROL_RE.finditer(text))
        assert matches == []

    def test_matches_all_families(self):
        from ingest import _CONTROL_RE, _NIST_FAMILIES
        for fam in _NIST_FAMILIES:
            text = f"{fam}-1 test control"
            full_matches = [m.group(0) for m in _CONTROL_RE.finditer(text)]
            assert full_matches == [f"{fam}-1"]


class TestIngestDocuments:
    @patch("ingest.glob.glob", return_value=[])
    def test_no_files_returns_no_files_status(self, mock_glob):
        from ingest import ingest_documents
        result = ingest_documents()
        assert result["status"] == "no_files"

    @patch("ingest.FAISS")
    @patch("ingest.get_embeddings")
    @patch("ingest.PyPDFLoader")
    @patch("ingest.glob.glob", return_value=["/fake/docs/nist.pdf"])
    def test_success_creates_index(self, mock_glob, mock_loader_cls, mock_emb, mock_faiss):
        mock_doc = MagicMock()
        mock_doc.page_content = "AC-2 Account Management is a control."
        mock_doc.metadata = {"source": "nist.pdf", "page": 42}

        mock_loader = MagicMock()
        mock_loader.load.return_value = [mock_doc]
        mock_loader_cls.return_value = mock_loader

        mock_vs = MagicMock()
        mock_faiss.from_documents.return_value = mock_vs

        from ingest import ingest_documents
        result = ingest_documents()

        assert result["status"] == "success"
        assert result["total_chunks"] > 0
        mock_vs.save_local.assert_called_once()

    @patch("ingest.FAISS")
    @patch("ingest.get_embeddings")
    @patch("ingest.PyPDFLoader")
    @patch("ingest.glob.glob", return_value=["/fake/docs/nist.pdf"])
    def test_enriches_metadata(self, mock_glob, mock_loader_cls, mock_emb, mock_faiss):
        mock_doc = MagicMock()
        mock_doc.page_content = "AC-2 Account Management and AC-3 Access Enforcement."
        mock_doc.metadata = {"source": "nist.pdf", "page": 10}

        mock_loader = MagicMock()
        mock_loader.load.return_value = [mock_doc]
        mock_loader_cls.return_value = mock_loader

        mock_faiss.from_documents.return_value = MagicMock()

        from ingest import ingest_documents
        ingest_documents()

        # Check that from_documents was called with enriched chunks
        call_args = mock_faiss.from_documents.call_args
        chunks = call_args[0][0]
        assert len(chunks) > 0
        first_chunk = chunks[0]
        assert "control_ids" in first_chunk.metadata
        assert "control_family" in first_chunk.metadata
