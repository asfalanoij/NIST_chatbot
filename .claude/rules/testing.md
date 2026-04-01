# Testing Standards

## Non-Negotiable Rules

- 38+ pytest tests must pass before ANY commit
- Target: 80%+ line coverage on backend Python files
- Tests run via: `cd backend && ./venv/bin/python -m pytest tests/ -v`

## Mock Boundaries

- Mock `Orchestrator` via `patch("agents.Orchestrator")` — NOT `patch("app.Orchestrator")`
- Mock LLM calls at the chain level, not at the HTTP level
- Never mock the SQLite interaction log — use `tmp_path` fixture for real DB tests
- Never mock FAISS in unit tests for `interaction_log.py` or `cache.py`

## Test File Map

| File | Tests it covers |
|------|----------------|
| `tests/test_app.py` | Flask endpoints, auth, rate limits |
| `tests/test_agents.py` | Orchestrator routing, agent selection |
| `tests/test_rag_engine.py` | RAGEngine retrieval, L2 threshold |
| `tests/test_schemas.py` | Pydantic validation, word-limit truncation |
| `tests/test_cache.py` | LRU cache hits/misses/TTL expiry |
| `tests/test_interaction_log.py` | SQLite write/read/stats |

## TDD Workflow

1. Write test → RED (test fails, implementation missing)
2. Implement → GREEN (test passes)
3. Refactor → IMPROVE (clean up without breaking tests)

Always use `tdd-guide` agent before writing new modules.
