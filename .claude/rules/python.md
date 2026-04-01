# Python Standards

## Logging

- Use `logging.getLogger(__name__)` — never `print()`
- Log levels: DEBUG for per-request detail, INFO for startup/config, WARNING for degraded state, ERROR for exceptions
- Always include structured context: `logger.info("Loaded index", extra={"vectors": n})`

## Type Hints

- All function signatures must have type hints (parameters + return type)
- Use `from __future__ import annotations` for forward references
- Prefer `list[str]` over `List[str]` (Python 3.10+)

## Pydantic

- All LLM input/output must go through Pydantic models (see `backend/schemas.py`)
- Use `model_dump()` not `.dict()` (Pydantic v2)
- Validators on `answer`: truncate at sentence boundary if > 250 words

## Error Handling

- Never silently swallow exceptions
- Wrap LLM calls in try/except; log the error and return a safe fallback
- Include error context in logs: `logger.error("LLM call failed", exc_info=True, extra={"agent": agent_id})`

## File Size

- Max 400 lines per file; split by responsibility if growing larger
- `rag_engine.py` owns retrieval; `agents.py` owns routing + orchestration; `app.py` owns HTTP
