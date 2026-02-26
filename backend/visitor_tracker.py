import os
import sqlite3
from datetime import datetime, timezone


DB_PATH = os.path.join(
    os.path.dirname(__file__),
    os.environ.get("VISITOR_DB_PATH", "visitors.db"),
)


def _get_db():
    """Get a SQLite connection, creating the table if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            user_agent TEXT,
            visited_at TEXT NOT NULL,
            path TEXT
        )
        """
    )
    conn.commit()
    return conn


def track_visit(ip_address, user_agent="", path="/"):
    """Record a visitor hit."""
    conn = _get_db()
    try:
        conn.execute(
            "INSERT INTO visitors (ip_address, user_agent, visited_at, path) VALUES (?, ?, ?, ?)",
            (ip_address, user_agent, datetime.now(timezone.utc).isoformat(), path),
        )
        conn.commit()
    finally:
        conn.close()


def get_visitor_counts():
    """Return unique visitor and total visit counts."""
    conn = _get_db()
    try:
        unique = conn.execute("SELECT COUNT(DISTINCT ip_address) FROM visitors").fetchone()[0]
        total = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        return {"unique_visitors": unique, "total_visits": total}
    finally:
        conn.close()
