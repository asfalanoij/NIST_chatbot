# /project:qa — Quality Assurance Agent

Run a 16-point QA check on the NIST chatbot backend before any deploy.

## Checklist

### Code Quality
1. [ ] No `print()` statements — all logging uses `logging` module
2. [ ] All functions have type hints
3. [ ] No hardcoded secrets or API keys
4. [ ] Files under 400 lines

### API Contract
5. [ ] `/api/chat` returns `answer`, `sources`, `agent_name`, `agent_id`
6. [ ] `/api/health` checks DB + FAISS and returns status
7. [ ] Rate limiting active on `/api/chat` (10/min) and `/api/ingest` (5/min)
8. [ ] `@require_api_key` on all endpoints

### RAG Quality
9. [ ] FAISS index loads without error
10. [ ] Test query "What is AC-2?" returns L2 score < 1.0
11. [ ] Test query "What is the weather?" is rejected (L2 > 1.5)
12. [ ] Answer contains at least 1 `[p.XX]` citation

### Tests
13. [ ] `make test-backend` passes (38+ tests, 0 failures)
14. [ ] No skipped tests without documented reason

### Security
15. [ ] `pip-audit` shows no critical CVEs
16. [ ] `.env` not committed; `interaction_log.db` gitignored

## Usage

```bash
# Claude Code will run this check when you invoke /project:qa
make test-backend
backend/venv/bin/pip-audit
```
