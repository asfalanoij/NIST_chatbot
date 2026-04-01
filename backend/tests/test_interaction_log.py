import sqlite3
import pytest
from pathlib import Path


@pytest.fixture
def tmp_db(tmp_path):
    return tmp_path / "test_interactions.db"


def test_log_interaction_creates_db(tmp_db):
    """log_interaction() initialises the DB and returns a UUID."""
    from interaction_log import log_interaction
    record_id = log_interaction(
        question="What is AC-2?",
        answer="AC-2 is account management [p.123].",
        latency_ms=800,
        db_path=tmp_db,
    )
    assert len(record_id) == 36
    assert tmp_db.exists()


def test_log_interaction_stores_hash_not_question(tmp_db):
    """The raw question text is NOT stored; only its hash is."""
    from interaction_log import log_interaction
    log_interaction(
        question="What is AC-2?",
        answer="Some answer.",
        latency_ms=500,
        db_path=tmp_db,
    )
    conn = sqlite3.connect(str(tmp_db))
    row = conn.execute("SELECT question_hash FROM interactions").fetchone()
    conn.close()
    assert row[0] != "What is AC-2?"
    assert len(row[0]) == 12  # sha256[:12]


def test_citation_count_extracted(tmp_db):
    """citation_count counts [p.XX] patterns in the answer."""
    from interaction_log import log_interaction
    log_interaction(
        question="AC-2 details",
        answer="See [p.42] and also [p.99] for context.",
        latency_ms=600,
        db_path=tmp_db,
    )
    conn = sqlite3.connect(str(tmp_db))
    row = conn.execute("SELECT citation_count FROM interactions").fetchone()
    conn.close()
    assert row[0] == 2


def test_get_stats_empty_db(tmp_db):
    """get_stats() works on an empty DB and returns zeros."""
    from interaction_log import get_stats, init_db
    init_db(tmp_db)
    stats = get_stats(tmp_db)
    assert stats["total_interactions"] == 0
    assert stats["cache_hit_rate"] == 0.0
    assert stats["avg_latency_ms"] == 0.0


def test_get_stats_after_interactions(tmp_db):
    """get_stats() returns correct aggregates after logging interactions."""
    from interaction_log import log_interaction, get_stats
    log_interaction("Q1", "Answer one [p.1].", 1000, cached=False, agent_id="NIST", db_path=tmp_db)
    log_interaction("Q2", "Answer two.", 2000, cached=True, agent_id="NIST", db_path=tmp_db)
    stats = get_stats(tmp_db)
    assert stats["total_interactions"] == 2
    assert stats["cache_hit_rate"] == 0.5
    assert stats["avg_latency_ms"] == 1500.0
    assert "NIST" in stats["agent_distribution"]


def test_schema_migration_guard(tmp_db):
    """Calling init_db() twice does not raise (IF NOT EXISTS guard)."""
    from interaction_log import init_db
    init_db(tmp_db)
    init_db(tmp_db)  # must not raise
