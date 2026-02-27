import logging
import os
import sqlite3
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

# SQLite fallback path for local dev
_SQLITE_PATH = os.path.join(
    os.path.dirname(__file__),
    os.environ.get("VISITOR_DB_PATH", "visitors.db"),
)

_CREATE_TABLE_PG = """
CREATE TABLE IF NOT EXISTS visitors (
    id SERIAL PRIMARY KEY,
    ip_address TEXT NOT NULL,
    user_agent TEXT,
    visited_at TEXT NOT NULL,
    path TEXT
)
"""

_CREATE_TABLE_SQLITE = """
CREATE TABLE IF NOT EXISTS visitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    user_agent TEXT,
    visited_at TEXT NOT NULL,
    path TEXT
)
"""


def _get_pg_conn():
    """Return a psycopg2 connection using DATABASE_URL."""
    import psycopg2
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    with conn.cursor() as cur:
        cur.execute(_CREATE_TABLE_PG)
    conn.commit()
    return conn


def _get_sqlite_conn():
    """Return a sqlite3 connection (local dev fallback)."""
    conn = sqlite3.connect(_SQLITE_PATH)
    conn.execute(_CREATE_TABLE_SQLITE)
    conn.commit()
    return conn


def _get_db():
    """Return a DB connection — PostgreSQL if DATABASE_URL is set, else SQLite."""
    if DATABASE_URL:
        return _get_pg_conn()
    return _get_sqlite_conn()


def track_visit(ip_address, user_agent="", path="/"):
    """Record a visitor hit."""
    conn = _get_db()
    try:
        if DATABASE_URL:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO visitors (ip_address, user_agent, visited_at, path) VALUES (%s, %s, %s, %s)",
                    (ip_address, user_agent, datetime.now(timezone.utc).isoformat(), path),
                )
            conn.commit()
        else:
            conn.execute(
                "INSERT INTO visitors (ip_address, user_agent, visited_at, path) VALUES (?, ?, ?, ?)",
                (ip_address, user_agent, datetime.now(timezone.utc).isoformat(), path),
            )
            conn.commit()
    except Exception:
        logger.exception("Failed to track visit")
    finally:
        conn.close()


def get_visitor_counts():
    """Return unique visitor and total visit counts."""
    conn = _get_db()
    try:
        if DATABASE_URL:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(DISTINCT ip_address) FROM visitors")
                unique = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM visitors")
                total = cur.fetchone()[0]
        else:
            unique = conn.execute("SELECT COUNT(DISTINCT ip_address) FROM visitors").fetchone()[0]
            total = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        return {"unique_visitors": unique, "total_visits": total}
    except Exception:
        logger.exception("Failed to get visitor counts")
        return {"unique_visitors": 0, "total_visits": 0, "error": "db_unavailable"}
    finally:
        conn.close()


def check_db_health():
    """Return True if the visitor database is reachable."""
    try:
        conn = _get_db()
        if DATABASE_URL:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        else:
            conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        logger.exception("DB health check failed")
        return False
