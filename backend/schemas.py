"""Pydantic v2 schemas for NIST chatbot request/response validation."""
from __future__ import annotations

import re
from pydantic import BaseModel, Field, field_validator, model_validator


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class HistoryEntry(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: list[HistoryEntry] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class SourceCitation(BaseModel):
    source: str
    page: str | int | None = None
    content_snippet: str = ""


class ValidationReport(BaseModel):
    citations_valid: int = 0
    citations_removed: list[str] = Field(default_factory=list)
    controls_ungrounded: list[str] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceCitation] = Field(default_factory=list)
    agent_name: str = ""
    agent_id: str = ""
    word_count: int = 0
    cached: bool = False
    latency_ms: int = 0
    validation: ValidationReport = Field(default_factory=ValidationReport)

    @field_validator("answer")
    @classmethod
    def truncate_at_word_limit(cls, v: str) -> str:
        """Truncate answer at sentence boundary if > 200 words."""
        words = v.split()
        if len(words) <= 200:
            return v
        # Find last sentence boundary within first 200 words
        truncated = " ".join(words[:200])
        # Try to end at a sentence boundary (. ! ?)
        match = re.search(r'[.!?][^.!?]*$', truncated)
        if match:
            return truncated[: match.start() + 1]
        return truncated

    @model_validator(mode="after")
    def compute_word_count(self) -> "ChatResponse":
        """Auto-compute word_count from answer if not explicitly set (0)."""
        if self.word_count == 0 and self.answer:
            self.word_count = len(self.answer.split())
        return self

    @classmethod
    def from_rag_result(
        cls,
        result: dict,
        *,
        cached: bool = False,
        latency_ms: int = 0,
    ) -> "ChatResponse":
        """Build a ChatResponse from a raw RAGEngine/Orchestrator result dict."""
        answer = result.get("answer", "")
        raw_sources = result.get("sources", [])
        sources = [
            SourceCitation(
                source=s.get("source", ""),
                page=s.get("page"),
                content_snippet=s.get("content_snippet", ""),
            )
            for s in raw_sources
        ]
        raw_validation = result.get("validation", {})
        validation = ValidationReport(**raw_validation) if raw_validation else ValidationReport()
        return cls(
            answer=answer,
            sources=sources,
            agent_name=result.get("agent_name", ""),
            agent_id=result.get("agent_id", ""),
            word_count=len(answer.split()),
            cached=cached,
            latency_ms=latency_ms,
            validation=validation,
        )


# ---------------------------------------------------------------------------
# Stats schema
# ---------------------------------------------------------------------------

class InteractionStats(BaseModel):
    total_interactions: int
    cache_hit_rate: float
    avg_latency_ms: float
    p95_latency_ms: int
    agent_distribution: dict[str, float]
    avg_relevance_score: float
    avg_word_count: float
    avg_citation_count: float
    avg_citations_valid: float = 0.0
    avg_citations_removed: float = 0.0
    avg_controls_ungrounded: float = 0.0
