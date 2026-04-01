"""LRU cache with TTL for stateless NIST chatbot queries."""
from __future__ import annotations

import hashlib
import logging
import time
from collections import OrderedDict
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_MAXSIZE = 128
_DEFAULT_TTL = 3600  # seconds


def _make_cache_key(question: str, agent_id: str) -> str:
    """Stable 16-char key: sha256 of normalised question + agent_id."""
    raw = question.lower().strip() + ":" + agent_id
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class LRUCache:
    """Thread-unsafe LRU cache with per-entry TTL.

    Only caches stateless queries (empty chat history).
    Returns ``{**result, "cached": True}`` on a hit.
    """

    def __init__(self, maxsize: int = _DEFAULT_MAXSIZE, ttl_seconds: int = _DEFAULT_TTL) -> None:
        self._maxsize = maxsize
        self._ttl = ttl_seconds
        self._store: OrderedDict[str, tuple[float, dict]] = OrderedDict()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, question: str, agent_id: str) -> dict | None:
        """Return cached result (with cached=True) or None on miss/expiry."""
        key = _make_cache_key(question, agent_id)
        if key not in self._store:
            return None
        inserted_at, result = self._store[key]
        if time.monotonic() - inserted_at > self._ttl:
            del self._store[key]
            logger.debug("Cache TTL expired for key %s", key)
            return None
        # Move to end (most recently used)
        self._store.move_to_end(key)
        logger.debug("Cache HIT key=%s", key)
        return {**result, "cached": True}

    def set(self, question: str, agent_id: str, result: dict) -> None:
        """Store result under the computed cache key."""
        key = _make_cache_key(question, agent_id)
        self._store[key] = (time.monotonic(), result)
        self._store.move_to_end(key)
        if len(self._store) > self._maxsize:
            evicted = self._store.popitem(last=False)
            logger.debug("Cache evicted LRU key %s", evicted[0])

    def clear(self) -> None:
        self._store.clear()

    @property
    def size(self) -> int:
        return len(self._store)
