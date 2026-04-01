import sqlite3
import uuid
import hashlib
import json
import logging
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "interaction_log.db"
logger = logging.getLogger(__name__)


@dataclass
class InteractionRecord:
    id: str
    timestamp: str           # ISO 8601 UTC
    question_hash: str       # sha256[:12] — frequency analysis without PII
    session_id: str
    agent_id: str
    agent_name: str
    answer: str
    word_count: int
    citation_count: int      # count of [p.XX] patterns in answer
    sources_json: str        # JSON array of {source, page, snippet}
    latency_ms: int
    cached: bool
    relevance_score: float   # L2 distance of top-1 chunk (lower = more relevant)
    llm_backend: str         # "gemini" or "ollama"


_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS interactions (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    question_hash TEXT NOT NULL,
    session_id TEXT,
    agent_id TEXT,
    agent_name TEXT,
    answer TEXT,
    word_count INTEGER,
    citation_count INTEGER,
    sources_json TEXT,
    latency_ms INTEGER,
    cached INTEGER DEFAULT 0,
    relevance_score REAL,
    llm_backend TEXT
);
CREATE INDEX IF NOT EXISTS idx_agent ON interactions(agent_id);
CREATE INDEX IF NOT EXISTS idx_timestamp ON interactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_hash ON interactions(question_hash);
"""


def _get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    """Initialize the interaction log database and schema."""
    with _get_connection(db_path) as conn:
        conn.executescript(_CREATE_TABLE_SQL)


def _hash_question(question: str) -> str:
    return hashlib.sha256(question.encode()).hexdigest()[:12]


def _count_citations(answer: str) -> int:
    return len(re.findall(r'\[p\.\d+\]', answer))


def log_interaction(
    question: str,
    answer: str,
    latency_ms: int,
    session_id: str = "",
    agent_id: str = "",
    agent_name: str = "",
    sources: list | None = None,
    cached: bool = False,
    relevance_score: float = 0.0,
    llm_backend: str = "gemini",
    db_path: Path = DB_PATH,
) -> str:
    """Write one interaction record. Returns the record ID."""
    init_db(db_path)
    record = InteractionRecord(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        question_hash=_hash_question(question),
        session_id=session_id or str(uuid.uuid4()),
        agent_id=agent_id,
        agent_name=agent_name,
        answer=answer,
        word_count=len(answer.split()),
        citation_count=_count_citations(answer),
        sources_json=json.dumps(sources or []),
        latency_ms=latency_ms,
        cached=cached,
        relevance_score=relevance_score,
        llm_backend=llm_backend,
    )
    row = asdict(record)
    row["cached"] = int(row["cached"])
    with _get_connection(db_path) as conn:
        conn.execute(
            """INSERT INTO interactions
               (id, timestamp, question_hash, session_id, agent_id, agent_name,
                answer, word_count, citation_count, sources_json,
                latency_ms, cached, relevance_score, llm_backend)
               VALUES
               (:id, :timestamp, :question_hash, :session_id, :agent_id, :agent_name,
                :answer, :word_count, :citation_count, :sources_json,
                :latency_ms, :cached, :relevance_score, :llm_backend)""",
            row,
        )
    logger.debug("Logged interaction %s (latency=%dms)", record.id, latency_ms)
    return record.id


def get_stats(db_path: Path = DB_PATH) -> dict:
    """Return aggregate stats. Safe to call even if DB is empty."""
    init_db(db_path)
    with _get_connection(db_path) as conn:
        row = conn.execute("""
            SELECT
                COUNT(*) AS total_interactions,
                AVG(latency_ms) AS avg_latency_ms,
                SUM(CASE WHEN cached = 1 THEN 1 ELSE 0 END) * 1.0 / MAX(COUNT(*), 1) AS cache_hit_rate,
                AVG(relevance_score) AS avg_relevance_score,
                AVG(word_count) AS avg_word_count,
                AVG(citation_count) AS avg_citation_count
            FROM interactions
        """).fetchone()

        agent_rows = conn.execute("""
            SELECT agent_id, COUNT(*) AS cnt FROM interactions
            WHERE agent_id != ''
            GROUP BY agent_id
        """).fetchall()

    total = row["total_interactions"] or 0
    agent_dist = {r["agent_id"]: round(r["cnt"] / max(total, 1), 4) for r in agent_rows}

    p95 = 0
    if total > 0:
        with _get_connection(db_path) as conn:
            latencies = [r[0] for r in conn.execute(
                "SELECT latency_ms FROM interactions ORDER BY latency_ms"
            ).fetchall()]
        idx = max(0, int(len(latencies) * 0.95) - 1)
        p95 = latencies[idx]

    return {
        "total_interactions": total,
        "cache_hit_rate": round(row["cache_hit_rate"] or 0.0, 4),
        "avg_latency_ms": round(row["avg_latency_ms"] or 0.0, 1),
        "p95_latency_ms": p95,
        "agent_distribution": agent_dist,
        "avg_relevance_score": round(row["avg_relevance_score"] or 0.0, 4),
        "avg_word_count": round(row["avg_word_count"] or 0.0, 1),
        "avg_citation_count": round(row["avg_citation_count"] or 0.0, 2),
    }
