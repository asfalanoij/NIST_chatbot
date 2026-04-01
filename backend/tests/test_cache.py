import time
import pytest
from cache import LRUCache, _make_cache_key


class TestCacheKey:
    def test_key_is_16_chars(self):
        key = _make_cache_key("What is AC-2?", "NIST_SPECIALIST")
        assert len(key) == 16

    def test_same_input_same_key(self):
        k1 = _make_cache_key("What is AC-2?", "NIST_SPECIALIST")
        k2 = _make_cache_key("What is AC-2?", "NIST_SPECIALIST")
        assert k1 == k2

    def test_case_insensitive_normalisation(self):
        k1 = _make_cache_key("What is AC-2?", "NIST_SPECIALIST")
        k2 = _make_cache_key("WHAT IS AC-2?", "NIST_SPECIALIST")
        assert k1 == k2

    def test_different_agents_different_keys(self):
        k1 = _make_cache_key("What is AC-2?", "NIST_SPECIALIST")
        k2 = _make_cache_key("What is AC-2?", "AUDIT_SPECIALIST")
        assert k1 != k2


class TestLRUCache:
    def test_miss_returns_none(self):
        cache = LRUCache()
        assert cache.get("What is AC-2?", "NIST_SPECIALIST") is None

    def test_set_then_get_returns_result(self):
        cache = LRUCache()
        result = {"answer": "AC-2 is account management.", "sources": []}
        cache.set("What is AC-2?", "NIST_SPECIALIST", result)
        hit = cache.get("What is AC-2?", "NIST_SPECIALIST")
        assert hit is not None
        assert hit["answer"] == "AC-2 is account management."
        assert hit["cached"] is True

    def test_hit_does_not_mutate_original(self):
        cache = LRUCache()
        result = {"answer": "answer", "sources": [], "cached": False}
        cache.set("q", "agent", result)
        hit = cache.get("q", "agent")
        # Original must be unmodified
        assert result["cached"] is False
        assert hit["cached"] is True

    def test_ttl_expiry(self):
        cache = LRUCache(ttl_seconds=0)  # expires immediately
        cache.set("q", "agent", {"answer": "x"})
        time.sleep(0.01)
        assert cache.get("q", "agent") is None

    def test_maxsize_evicts_lru(self):
        cache = LRUCache(maxsize=2)
        cache.set("q1", "a", {"answer": "1"})
        cache.set("q2", "a", {"answer": "2"})
        # Access q1 to make q2 the LRU
        cache.get("q1", "a")
        # Add q3 — q2 should be evicted
        cache.set("q3", "a", {"answer": "3"})
        assert cache.get("q2", "a") is None
        assert cache.get("q1", "a") is not None
        assert cache.get("q3", "a") is not None

    def test_clear(self):
        cache = LRUCache()
        cache.set("q", "a", {"answer": "x"})
        cache.clear()
        assert cache.size == 0
        assert cache.get("q", "a") is None
