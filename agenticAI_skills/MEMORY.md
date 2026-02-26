# MEMORY.md — NIST 800-53 Chatbot v02
> Auto-loaded each session. Keep under 150 lines.

## Current State
- **Sprint**: 6 complete
- **QA Score**: 16/16 (was 14/16)
- **Security Score**: 8/10
- **NIST/RAG Coverage**: 11/11
- **Auth Score**: 8/8
- **CI/CD Score**: 9/10 (missing GH Actions)
- **Load Test**: 4/4 (health 2ms, chat 5.5s)
- **Export Readiness**: 6/6
- **Tests**: 38/38 pass (was 34 — added QA + DevSecOps agent tests)
- **Frontend**: Builds clean (0 warnings)
- **Build Agents**: 13 (was 8 — added 5 new)

## Architecture
- **Runtime Agents** (7): NIST Controls, Audit, Risk, Compliance, PM, QA, DevSecOps — in `backend/agents.py`
- **Build Agents** (13): QA, DevSecOps, NIST Expert, Data Scientist, PM, E2E Test, Context Optimizer, Visitor Tracker, **API Auth, API Load Test, RAG Evaluator, Chat Export, CI/CD**
- **LLM Fallback**: Ollama → Gemini via `get_llm()` in `rag_engine.py`
- **Embedding Fallback**: Ollama → Gemini via `get_embeddings()` in `rag_engine.py` (NEW)
- **API Auth**: `@require_api_key` decorator on `/api/chat` + `/api/ingest` (NEW)
- **Visitor Tracking**: SQLite via `visitor_tracker.py`, endpoint `/api/visitors/count`

## Key Files
| File | Purpose |
|------|---------|
| `backend/app.py` | Flask API + `@require_api_key` auth decorator |
| `backend/rag_engine.py` | RAG engine + `get_llm()` + `get_embeddings()` fallback |
| `backend/agents.py` | 7 runtime agents + Orchestrator |
| `backend/ingest.py` | PDF ingestion using `get_embeddings()` |
| `backend/visitor_tracker.py` | SQLite visitor tracking |
| `backend/tests/` | 38 pytest tests (api, agents, rag_engine, auth) |
| `frontend/src/components/ChatLayout.tsx` | Main UI + X-API-Key header |
| `agenticAI_skills/antigravity.sh` | Build agent dispatcher (13 agents) |

## Recent Changes (2026-02-17 — Sprint 6)
1. **2 new runtime agents** (5→7): QA & Test Strategy, DevSecOps & Pipeline Security
2. **Keyword routing expanded**: 13 QA keywords + 15 DevSecOps keywords, no overlap with existing agents
3. **Tests**: 34→38. Added QA/DevSecOps keyword + routing tests.
4. **Frontend**: constants.ts + ChatLayout.tsx updated with 7 agent cards
5. **Sprint 6 docs**: Strategy table, metric history, Sprint 7 candidates
6. **Index rebuild still needed**: Run `make ingest` to create compatible index.

## Decisions Made
- macOS bash 3.2: No associative arrays. Use `case` statements in shell scripts.
- Keyword routing: "compliance" matches COMPLIANCE_SPECIALIST before PM_AGENT.
- CORS: Env-configured via CORS_ORIGINS (not wildcard `*`)
- Datetime: Use `datetime.now(timezone.utc)` (not deprecated `utcnow()`)
- Auth: Dev mode skips auth when API_KEY is unset (safe for local dev)
- Embeddings: Single `get_embeddings()` function ensures ingest + query always match

## Last Session
- **Date**: 2026-02-17 (Sprint 6)
- **Type**: Agent Expansion (5→7 runtime agents)
- **Changes**: QA + DevSecOps agents, 38 tests, frontend 7-agent sidebar, Sprint 6 docs

-  **Date**: 2026-02-17 (session cache)
-  **Changes**: Resume this session with: claude --resume c5446da8-3047-48af-9486-6a4180610e02
## Remaining (Sprint 7 Candidates)
- [ ] ISO 27001 + ISO 27005 + CSF 2.0 + NIST 800-53 cross-mapping
- [ ] Downloadable Sankey Diagram CSV
- [ ] Re-ingest documents with correct embeddings (`make ingest`)
- [ ] GitHub Actions CI workflow (`.github/workflows/ci.yml`)
- [ ] Git tag v2.0.0
