import pytest
from pydantic import ValidationError
from schemas import ChatResponse, QueryRequest, InteractionStats, HistoryEntry, SourceCitation


class TestQueryRequest:
    def test_valid_message(self):
        req = QueryRequest(message="What is AC-2?")
        assert req.message == "What is AC-2?"
        assert req.history == []

    def test_message_too_short(self):
        with pytest.raises(ValidationError):
            QueryRequest(message="")

    def test_message_too_long(self):
        with pytest.raises(ValidationError):
            QueryRequest(message="x" * 2001)

    def test_history_entries(self):
        req = QueryRequest(
            message="Follow up",
            history=[{"role": "user", "content": "What is AC-2?"}, {"role": "assistant", "content": "AC-2 is..."}],
        )
        assert len(req.history) == 2
        assert req.history[0].role == "user"


class TestChatResponse:
    def test_basic_response(self):
        resp = ChatResponse(answer="AC-2 is account management [p.42].")
        assert resp.answer == "AC-2 is account management [p.42]."
        assert resp.sources == []
        assert resp.cached is False

    def test_answer_within_limit_not_truncated(self):
        short = "Short answer. " * 10  # well under 200 words
        resp = ChatResponse(answer=short)
        assert resp.answer == short

    def test_answer_truncated_at_200_words(self):
        # 300 words — should be truncated
        long_answer = ("word " * 300).strip()
        resp = ChatResponse(answer=long_answer)
        assert len(resp.answer.split()) <= 200

    def test_truncation_at_sentence_boundary(self):
        # Build an answer that is 210 words, with a sentence end at word 150
        first_part = ("word " * 149).strip() + ". "
        second_part = ("extra " * 61).strip()
        long_answer = first_part + second_part
        resp = ChatResponse(answer=long_answer)
        # Should end with a period (sentence boundary)
        assert resp.answer.endswith(".")

    def test_from_rag_result(self):
        raw = {
            "answer": "AC-2 controls account management [p.42].",
            "sources": [{"source": "nist.pdf", "page": 42, "content_snippet": "AC-2..."}],
            "agent_name": "NIST Controls Specialist",
            "agent_id": "NIST_SPECIALIST",
        }
        resp = ChatResponse.from_rag_result(raw, cached=True, latency_ms=800)
        assert resp.agent_id == "NIST_SPECIALIST"
        assert resp.cached is True
        assert resp.latency_ms == 800
        assert resp.word_count > 0
        assert len(resp.sources) == 1

    def test_word_count_computed(self):
        resp = ChatResponse(answer="one two three four five")
        assert resp.word_count == 5


class TestInteractionStats:
    def test_valid_stats(self):
        stats = InteractionStats(
            total_interactions=100,
            cache_hit_rate=0.35,
            avg_latency_ms=1500.0,
            p95_latency_ms=4200,
            agent_distribution={"NIST_SPECIALIST": 0.6},
            avg_relevance_score=0.82,
            avg_word_count=145.3,
            avg_citation_count=2.1,
        )
        assert stats.total_interactions == 100
        assert stats.cache_hit_rate == 0.35
