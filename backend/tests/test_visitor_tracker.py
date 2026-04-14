import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestTrackVisit:
    def test_creates_db_and_inserts_row(self, tmp_path, monkeypatch):
        db_path = str(tmp_path / "test_visitors.db")
        monkeypatch.setattr("visitor_tracker._SQLITE_PATH", db_path)
        monkeypatch.setattr("visitor_tracker.DATABASE_URL", None)

        import visitor_tracker
        visitor_tracker.track_visit(ip_address="1.2.3.4", user_agent="test-ua", path="/api/chat")

        import sqlite3
        conn = sqlite3.connect(db_path)
        rows = conn.execute("SELECT * FROM visitors").fetchall()
        conn.close()
        assert len(rows) == 1

    def test_records_correct_fields(self, tmp_path, monkeypatch):
        db_path = str(tmp_path / "test_visitors.db")
        monkeypatch.setattr("visitor_tracker._SQLITE_PATH", db_path)
        monkeypatch.setattr("visitor_tracker.DATABASE_URL", None)

        import visitor_tracker
        visitor_tracker.track_visit(ip_address="10.0.0.1", user_agent="Mozilla/5.0", path="/test")

        import sqlite3
        conn = sqlite3.connect(db_path)
        row = conn.execute("SELECT ip_address, user_agent, path FROM visitors").fetchone()
        conn.close()
        assert row[0] == "10.0.0.1"
        assert row[1] == "Mozilla/5.0"
        assert row[2] == "/test"

    def test_db_failure_does_not_raise(self, monkeypatch):
        monkeypatch.setattr("visitor_tracker.DATABASE_URL", None)
        monkeypatch.setattr("visitor_tracker._get_db", MagicMock(side_effect=RuntimeError("boom")))

        import visitor_tracker
        # Should not raise — silently fails
        result = visitor_tracker.track_visit(ip_address="1.2.3.4")
        assert result is None


class TestGetVisitorCounts:
    def test_empty_db(self, tmp_path, monkeypatch):
        db_path = str(tmp_path / "test_visitors.db")
        monkeypatch.setattr("visitor_tracker._SQLITE_PATH", db_path)
        monkeypatch.setattr("visitor_tracker.DATABASE_URL", None)

        import visitor_tracker
        # Initialize the table
        visitor_tracker._get_sqlite_conn().close()

        counts = visitor_tracker.get_visitor_counts()
        assert counts["unique_visitors"] == 0
        assert counts["total_visits"] == 0

    def test_after_visits(self, tmp_path, monkeypatch):
        db_path = str(tmp_path / "test_visitors.db")
        monkeypatch.setattr("visitor_tracker._SQLITE_PATH", db_path)
        monkeypatch.setattr("visitor_tracker.DATABASE_URL", None)

        import visitor_tracker
        visitor_tracker.track_visit(ip_address="1.1.1.1")
        visitor_tracker.track_visit(ip_address="2.2.2.2")
        visitor_tracker.track_visit(ip_address="1.1.1.1")  # duplicate IP

        counts = visitor_tracker.get_visitor_counts()
        assert counts["unique_visitors"] == 2
        assert counts["total_visits"] == 3

    def test_db_failure_returns_error(self, monkeypatch):
        monkeypatch.setattr("visitor_tracker.DATABASE_URL", None)
        monkeypatch.setattr("visitor_tracker._get_db", MagicMock(side_effect=RuntimeError("boom")))

        import visitor_tracker
        counts = visitor_tracker.get_visitor_counts()
        assert "error" in counts
        assert counts["unique_visitors"] == 0


class TestCheckDbHealth:
    def test_returns_true(self, tmp_path, monkeypatch):
        db_path = str(tmp_path / "test_visitors.db")
        monkeypatch.setattr("visitor_tracker._SQLITE_PATH", db_path)
        monkeypatch.setattr("visitor_tracker.DATABASE_URL", None)

        import visitor_tracker
        assert visitor_tracker.check_db_health() is True

    def test_returns_false_on_failure(self, monkeypatch):
        monkeypatch.setattr("visitor_tracker.DATABASE_URL", None)
        monkeypatch.setattr("visitor_tracker._get_db", MagicMock(side_effect=RuntimeError("boom")))

        import visitor_tracker
        assert visitor_tracker.check_db_health() is False
