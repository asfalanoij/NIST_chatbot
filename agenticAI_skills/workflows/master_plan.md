# Master Plan — NIST 800-53 Chatbot v02

## Sprint Roadmap

### Sprint 1: Security + Agent Skeleton [COMPLETE]
- Created `agenticAI_skills/` framework: `antigravity.sh` dispatcher + `utils.sh`
- Built 8 build-time agents: QA, DevSecOps, NIST Expert, Data Scientist, PM, E2E Test, Context Optimizer, Visitor Tracker
- Created `.env.example` with all config keys
- Updated `.gitignore` (*.db, .logs/, README_local.md, .env.local)
- Added Gemini fallback via `get_llm()` in `rag_engine.py` and `agents.py`
- Added `langchain-google-genai` to requirements.txt
- Fixed bash 3.2 compatibility (no associative arrays on macOS)

### Sprint 2: Testing Infrastructure [COMPLETE]
- Created `backend/tests/` with conftest.py, test_api.py, test_agents.py, test_rag_engine.py
- 26 tests all passing
- Updated Makefile with `test-backend`, `test-frontend`, `test`, `qa`, `scan`, `maturity` targets

### Sprint 3: Visitor Tracking + API Robustness [COMPLETE]
- Created `backend/visitor_tracker.py` (SQLite: IP + User-Agent + timestamp)
- Added `/api/visitors/count` endpoint
- Added `@before_request` visitor tracking on `/api/chat`
- CORS configured via `CORS_ORIGINS` env var (not wildcard)
- Flask debug mode via `FLASK_DEBUG` env var
- `SECRET_KEY` from env
- `/api/health` now reports `llm_backend` (ollama vs gemini)
- Frontend sidebar footer shows visitor count badge

### Sprint 4: Documentation + Context System [COMPLETE]
- Created 3-layer context system:
  - Layer 1: `MEMORY.md` — auto-loaded session context
  - Layer 2: `context_map.md` — token-optimized project map
  - Layer 3: `workflows/master_plan.md` — this file
- Raw agent output logs captured in `.logs/session-2026-02-16/`
- Updated README.md for GitHub

### Sprint 5: Auth, Embeddings & New Agents [COMPLETE]

#### Completed (2026-02-17)
- [x] **API Authentication**: `@require_api_key` decorator on `/api/chat` + `/api/ingest`
  - Reads `API_KEY` from env; empty = dev mode (no auth)
  - Returns 401 with JSON error on invalid/missing key
  - `/api/health` and `/api/visitors/count` remain open
  - Frontend sends `X-API-Key` header from `VITE_API_KEY`
- [x] **Embedding dimension fix**: Added `get_embeddings()` in `rag_engine.py`
  - Gemini: `GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")` → 3072-dim
  - Ollama: `OllamaEmbeddings(model=OLLAMA_MODEL)` → 768-dim
  - Both `ingest.py` and `rag_engine.py` use same function → no mismatch
- [x] **Test suite expanded**: 26 → 34 tests
  - 6 new auth tests (TestApiKeyAuth): reject/accept/dev-mode/health-unprotected
  - 2 new embedding tests (TestGetEmbeddings): Ollama default, Gemini fallback
  - Fixed conftest mock fragility (Orchestrator mock was overwritten by reload)
- [x] **5 new build agents** (8 → 13 total):
  - `api-auth`: 8-point auth verification (decorator presence, live 401/200 tests)
  - `api-loadtest`: Endpoint stress test (health avg latency, concurrent requests, chat timing)
  - `rag-evaluator`: 11-point retrieval quality (index health, 5 live test queries with keyword matching)
  - `chat-export`: 6-point export readiness (citations, metadata, markdown support)
  - `cicd`: 10-point CI/CD pipeline readiness (tests, build, GitHub Actions, deps)
- [x] **Makefile updated**: Added `auth`, `loadtest`, `rag-eval`, `export-check`, `cicd` targets
- [x] **.env.example updated**: Added `API_KEY`, `GEMINI_EMBEDDING_MODEL`

#### Carried Forward
- [ ] Re-ingest documents with correct embeddings (`make ingest`)
- [ ] Create GitHub Actions CI workflow (`.github/workflows/ci.yml`)
- [ ] Git tag v2.0.0

### Sprint 6: Agent Expansion [COMPLETE]

#### Completed (2026-02-17)
- [x] **2 new runtime agents** (5 → 7): QA & Test Strategy, DevSecOps & Pipeline Security
  - QA: test cases, validation criteria, coverage matrices, control testing methodology
  - DevSecOps: CI/CD hardening, SAST/DAST, container security, compliance-as-code
- [x] **Keyword routing**: 13 QA keywords + 15 DevSecOps keywords, no overlap with existing agents
- [x] **Tests expanded**: 34 → 38 (2 updated + 4 new routing tests)
- [x] **Frontend updated**: constants.ts + ChatLayout.tsx sidebar — 7 agent cards
- [x] **Sprint documentation**: strategy table, metric history, Sprint 7 candidates

#### Sprint 7 Candidates
- [ ] ISO 27001 + ISO 27005 + CSF 2.0 + NIST 800-53 cross-mapping
- [ ] Downloadable Sankey Diagram CSV
- [ ] GitHub Actions CI workflow (`.github/workflows/ci.yml`)
- [ ] Re-ingest with correct embeddings (`make ingest`)
- [ ] Git tag v2.0.0

## Sprint Strategy

| Sprint | Focus | Key Metrics |
|--------|-------|-------------|
| 1 | Foundation + Build Agents | 8 build agents, Gemini fallback |
| 2 | Testing Infrastructure | 26/26 tests |
| 3 | API Robustness | Visitor tracking, CORS, 4 endpoints |
| 4 | Documentation | 3-layer context system |
| 5 | Auth & Embeddings | 34/34 tests, 13 build agents, 100% maturity |
| 6 | Agent Expansion | 7 runtime agents, 38/38 tests |

## Metric History

| Date | QA | Security | NIST | Maturity | Tests | Agents |
|------|-----|----------|------|----------|-------|--------|
| 2026-02-16 | 14/16 | 8/10 | 10/10 | 75% | 26/26 | 8 |
| 2026-02-17 | 16/16 | 8/10 | 11/11 | 100% | 34/34 | 13 |
| 2026-02-17b | 16/16 | 8/10 | 11/11 | 100% | 38/38 | 13 |

## Agent Scorecard (2026-02-17)

| Agent | Skill | Score | Notes |
|-------|-------|-------|-------|
| qa | inspect | 16/16 | All green |
| devsecops | scan | 8/10 | Print statements, .env.example flag |
| rag-evaluator | evaluate | 11/11 | 5/5 live retrieval tests passed |
| api-auth | verify | 8/8 | All checks passed (dev mode) |
| api-loadtest | stress | 4/4 | Health 2ms, Chat 5.5s |
| chat-export | check | 6/6 | Ready for UI implementation |
| cicd | check | 9/10 | Missing GitHub Actions workflow |
| pm | maturity | 100% | All 11 indicators green |
