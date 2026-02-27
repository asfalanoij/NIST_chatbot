import json
import csv
import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from crossmap import get_crossmap, get_families, get_stats, generate_sankey_csv, CROSSMAP


class TestCrossmapModule:
    """Unit tests for the crossmap module."""

    def test_crossmap_has_entries(self):
        assert len(CROSSMAP) > 20

    def test_entry_structure(self):
        entry = CROSSMAP[0]
        assert "nist_id" in entry
        assert "nist_title" in entry
        assert "nist_family" in entry
        assert "iso27001" in entry
        assert "csf2" in entry
        assert "iso27005" in entry
        assert isinstance(entry["iso27001"], list)
        assert isinstance(entry["csf2"], list)
        assert isinstance(entry["iso27005"], list)

    def test_filter_by_family(self):
        results = get_crossmap(family="Access Control")
        assert len(results) > 0
        assert all(r["nist_family"] == "Access Control" for r in results)

    def test_filter_by_nist_id(self):
        results = get_crossmap(nist_id="AC-2")
        assert len(results) == 1
        assert results[0]["nist_id"] == "AC-2"

    def test_filter_by_framework(self):
        results = get_crossmap(framework="iso27001")
        assert len(results) > 0
        for r in results:
            assert "iso27001" in r
            assert "csf2" not in r

    def test_get_families(self):
        families = get_families()
        assert "Access Control" in families
        assert "Incident Response" in families
        assert len(families) >= 8

    def test_get_stats(self):
        stats = get_stats()
        assert stats["total_nist_controls"] > 20
        assert stats["nist_families"] >= 8
        assert stats["unique_iso27001_controls"] > 10
        assert stats["unique_csf2_categories"] > 5
        assert stats["unique_iso27005_clauses"] > 3

    def test_no_filter_returns_all(self):
        results = get_crossmap()
        assert len(results) == len(CROSSMAP)


class TestSankeyCSV:
    """Tests for Sankey diagram CSV generation."""

    def test_csv_has_header(self):
        csv_data = generate_sankey_csv()
        reader = csv.reader(io.StringIO(csv_data))
        header = next(reader)
        assert header == ["source", "target", "value"]

    def test_csv_has_rows(self):
        csv_data = generate_sankey_csv()
        reader = csv.reader(io.StringIO(csv_data))
        next(reader)  # skip header
        rows = list(reader)
        assert len(rows) > 50  # should have many mapping links

    def test_csv_source_format(self):
        csv_data = generate_sankey_csv()
        reader = csv.reader(io.StringIO(csv_data))
        next(reader)  # skip header
        for row in reader:
            assert row[0].startswith("NIST ")
            assert row[2] == "1"

    def test_csv_targets_include_all_frameworks(self):
        csv_data = generate_sankey_csv()
        reader = csv.reader(io.StringIO(csv_data))
        next(reader)
        targets = set(row[1].split()[0] for row in reader)
        assert "ISO" in targets  # ISO 27001
        assert "CSF" in targets  # CSF 2.0
        assert "ISO27005" in targets  # ISO 27005


class TestCrossmapEndpoints:
    """Test the crossmap API endpoints."""

    def test_crossmap_returns_200(self, app_client):
        response = app_client.get("/api/crossmap")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "mappings" in data
        assert "count" in data
        assert data["count"] > 0

    def test_crossmap_filter_family(self, app_client):
        response = app_client.get("/api/crossmap?family=Access+Control")
        assert response.status_code == 200
        data = json.loads(response.data)
        for m in data["mappings"]:
            assert m["nist_family"] == "Access Control"

    def test_crossmap_filter_nist_id(self, app_client):
        response = app_client.get("/api/crossmap?nist_id=AC-2")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["count"] == 1
        assert data["mappings"][0]["nist_id"] == "AC-2"

    def test_crossmap_filter_framework(self, app_client):
        response = app_client.get("/api/crossmap?framework=csf2")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "csf2" in data["mappings"][0]
        assert "iso27001" not in data["mappings"][0]

    def test_crossmap_families_endpoint(self, app_client):
        response = app_client.get("/api/crossmap/families")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "Access Control" in data["families"]

    def test_crossmap_stats_endpoint(self, app_client):
        response = app_client.get("/api/crossmap/stats")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["total_nist_controls"] > 20

    def test_sankey_csv_download(self, app_client):
        response = app_client.get("/api/crossmap/sankey")
        assert response.status_code == 200
        assert response.content_type == "text/csv; charset=utf-8"
        assert "attachment" in response.headers.get("Content-Disposition", "")
        # Verify it's valid CSV
        csv_text = response.data.decode("utf-8")
        reader = csv.reader(io.StringIO(csv_text))
        header = next(reader)
        assert header == ["source", "target", "value"]

    def test_crossmap_endpoints_not_protected(self, app_client):
        """Crossmap endpoints should be publicly accessible."""
        from unittest.mock import patch as mock_patch
        with mock_patch.dict(os.environ, {"API_KEY": "test-secret-key"}, clear=False):
            response = app_client.get("/api/crossmap")
            assert response.status_code == 200
            response = app_client.get("/api/crossmap/families")
            assert response.status_code == 200
            response = app_client.get("/api/crossmap/stats")
            assert response.status_code == 200
            response = app_client.get("/api/crossmap/sankey")
            assert response.status_code == 200
