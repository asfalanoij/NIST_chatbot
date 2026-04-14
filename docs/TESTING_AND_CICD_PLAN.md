# Testing Infrastructure & CI/CD Hardening

## Context

The lean architecture revamp (v03) is complete — 4 agents, faithfulness validation, gemini-embedding-001, 95 existing tests. But the testing and CI/CD infrastructure has significant gaps:

- **2 broken tests** blocking CI (wrong patch target after blueprint refactor, fixture name mismatch)
- **3 backend modules with ZERO tests**: `visitor_tracker.py` (129 lines), `ingest.py` (83 lines), `api/config.py` (25 lines)
- **Zero frontend tests**: no Vitest, no @testing-library/react, no test scripts
- **1 E2E smoke test** that only checks page title
- **No coverage enforcement** — 80% target exists in docs but is unenforced
- **CI E2E job fragile** — backend can't start without GEMINI_API_KEY in CI
- **docker-compose.prod.yml** has stale `text-embedding-004` embedding model
- **Dead code**: `ChatLayout.tsx` (225 lines, zero imports)
- **DRY violation**: `require_api_key` duplicated in `api/chat.py` and `api/health.py`

**Goal**: 0 broken tests, 80%+ backend coverage enforced in CI, frontend Vitest + RTL, meaningful E2E, hardened CI pipeline.

---

## Current State Audit

### Backend Tests (95 tests across 7 files)

| Test File | Count | Status |
|-----------|-------|--------|
| `test_api.py` | 24 | 23 pass, 1 broken (`test_error_response_does_not_leak_exception` — patches `app.orchestrator` but it moved to `api.chat.orchestrator`) |
| `test_agents.py` | 14 | All pass |
| `test_rag_engine.py` | 15 | All pass |
| `test_schemas.py` | 10 | All pass |
| `test_cache.py` | 8 | All pass |
| `test_interaction_log.py` | 6 | All pass |
| `test_crossmap.py` | 17 | All pass |
| `test_integration.py` | 1 | Broken (uses `client` fixture, conftest defines `app_client`) |

### Backend Coverage Gaps

| Module | Lines | Tests | Gap |
|--------|-------|-------|-----|
| `visitor_tracker.py` | 129 | ZERO | track_visit(), get_visitor_counts(), check_db_health(), SQLite fallback |
| `ingest.py` | 83 | ZERO | ingest_documents(), control ID regex, metadata enrichment |
| `api/config.py` | 25 | ZERO | /api/config/agents, /api/config/crossmap |
| `agents.py` | 219 | Partial | route_and_chat() only via Flask client; route_and_chat_stream() ZERO; cache interaction ZERO; LLM router fallback ZERO |
| `rag_engine.py` | 316 | Partial | chat() full path never tested with mocked index; chat_stream() ZERO; _history_to_messages() ZERO |
| `api/chat.py` | 120 | Partial | Some tested indirectly; _sanitise_session_id, stream error handling not directly tested |
| `api/health.py` | 66 | Partial | /api/interactions/stats, degraded health check not tested |

### Architectural Issues

1. **Orchestrator at module level in blueprints** — `api/chat.py` line 22 and `api/health.py` line 15 both create `Orchestrator()` at import time. Tests must patch before import. Current conftest uses fragile `importlib.reload` approach.
2. **`require_api_key` duplicated** — identical 11-line decorator in `api/chat.py` (lines 25-35) and `api/health.py` (lines 19-29).
3. **No `pytest-cov`** — 80% coverage target documented but unenforced. Makefile and CI run `pytest` without `--cov`.

### Frontend Tests: ZERO

- No Vitest, no Jest, no @testing-library/react installed
- No test scripts in `package.json` (only `dev`, `build`, `lint`, `preview`)
- No `.test.*` or `.spec.*` files in `frontend/src/`

### E2E Tests: 1 Smoke Test

**File**: `frontend/e2e/app.spec.ts`
```typescript
test('has title and loads config', async ({ page }) => {
  await page.goto('http://localhost:5173/');
  await expect(page).toHaveTitle(/NIST Chatbot/i);
  await expect(page.locator('text=Specialist Agents')).toBeVisible();
});
```

- Playwright config exists at `frontend/playwright.config.ts` (Chromium, auto-starts Vite, 2 retries in CI)
- Playwright NOT in `package.json` devDependencies (relies on npx download)

### CI/CD Pipeline (`.github/workflows/ci.yml`)

| Job | Trigger | What It Does | Issues |
|-----|---------|-------------|--------|
| `backend-tests` | push dev/main/v03, PRs to main | pip install + pytest | No coverage. 2 broken tests block pipeline. |
| `security` | After backend-tests | bandit + pip-audit | Blocked by broken tests upstream. |
| `frontend-build` | Same trigger | npm ci + npm run build | Build-only, no lint, no tests. |
| `e2e-tests` | After frontend-build + backend-tests | Start backend + Playwright | Backend crashes without GEMINI_API_KEY. |

### Deploy Pipeline (`.github/workflows/deploy.yml`)

- Trigger: push to main
- Action: Build frontend, SCP to VPS, docker-compose up

### Docker/Deployment

- `docker-compose.prod.yml` line 30: `GEMINI_EMBEDDING_MODEL: models/text-embedding-004` — **WRONG**, should be `models/gemini-embedding-001`
- `render.yaml`: Correct configuration
- `Dockerfile`: Downloads FAISS index from GitHub Release v2.0.0

### Dead Code

- `frontend/src/components/ChatLayout.tsx` — 225 lines, exported but never imported anywhere (confirmed by grep)

---

## Phase 0: Fix Broken Tests (P0 — unblocks CI)

**Estimated additions**: 0 new tests, 2 tests fixed

### 0a. Fix `test_error_response_does_not_leak_exception`

**File**: `backend/tests/test_api.py`

- **Current**: patches `app.orchestrator`
- **Fix**: change patch target to `api.chat.orchestrator`
- **Reason**: Orchestrator moved to `api/chat.py` module scope after blueprint refactor

### 0b. Fix `test_integration_health`

**File**: `backend/tests/test_integration.py`

- **Current**: `def test_integration_health(client):`
- **Fix**: `def test_integration_health(app_client):`
- **Reason**: conftest defines `app_client`, not `client`

### Verification

```bash
cd backend && ./venv/bin/python -m pytest tests/ -v
# Expected: all 95 tests pass
```

---

## Phase 1: Backend Test Infrastructure

**Estimated additions**: 3 new tests (auth), infrastructure changes

### 1a. Add `pytest-cov`

**File**: `backend/requirements-dev.txt`

Add: `pytest-cov>=6.0`

### 1b. Extract `require_api_key` to shared module

**New file**: `backend/api/auth.py`

Move the `require_api_key` decorator from `api/chat.py` (lines 25-35). Identical copy exists in `api/health.py` (lines 19-29).

**Modify**: `backend/api/chat.py` — `from api.auth import require_api_key`
**Modify**: `backend/api/health.py` — `from api.auth import require_api_key`

**New file**: `backend/tests/test_auth.py` (~3 tests)

- `test_no_api_key_env_passes_through` — empty `API_KEY` env = dev mode, decorator is no-op
- `test_wrong_key_returns_401` — `API_KEY` set, wrong key provided
- `test_correct_key_passes` — `API_KEY` set, correct key provided

### 1c. Refactor conftest for blueprint-aware patching

**File**: `backend/tests/conftest.py`

Replace `importlib.reload` approach with direct patching of `api.chat.orchestrator` and `api.health.orchestrator`. Steps:

1. Patch `agents.RAGEngine` and `agents.get_routing_llm` (prevents real LLM/embedding init)
2. Import `app` module and get `app.app`
3. Patch `api.chat.orchestrator` and `api.health.orchestrator` with mock Orchestrator instance
4. Set `TESTING=True` on the app
5. Yield `app.test_client()` inside the patch context

### Verification

```bash
cd backend && ./venv/bin/python -m pytest tests/ -v --cov=. --cov-report=term-missing
# Expected: all tests pass, coverage report visible
```

---

## Phase 2: Backend Unit Tests (~30 new tests)

### 2a. `test_visitor_tracker.py` (new file, ~8 tests)

**File**: `backend/tests/test_visitor_tracker.py`

Use `tmp_path` for SQLite, `monkeypatch.delenv("DATABASE_URL")` to force SQLite path, `monkeypatch.setattr("visitor_tracker._SQLITE_PATH", str(tmp_path / "test_visitors.db"))`.

| Test | What It Verifies |
|------|-----------------|
| `test_track_visit_creates_db_and_inserts_row` | Row count after one call |
| `test_track_visit_records_correct_fields` | ip_address, user_agent, path, visited_at populated |
| `test_get_visitor_counts_empty_db` | Returns `{unique_visitors: 0, total_visits: 0}` |
| `test_get_visitor_counts_after_visits` | 3 visits from 2 IPs → correct counts |
| `test_check_db_health_returns_true` | SQLite connection healthy |
| `test_check_db_health_returns_false_on_failure` | Patch `_get_db` to raise → returns False |
| `test_track_visit_db_failure_does_not_raise` | Patch `_get_db` to raise → returns None silently |
| `test_get_visitor_counts_db_failure_returns_error` | Patch `_get_db` to raise → error key in dict |

### 2b. `test_ingest.py` (new file, ~6 tests)

**File**: `backend/tests/test_ingest.py`

Mock `PyPDFLoader`, `FAISS.from_documents`, `get_embeddings`.

| Test | What It Verifies |
|------|-----------------|
| `test_ingest_no_files_returns_no_files_status` | mock `glob.glob` empty → `status == "no_files"` |
| `test_ingest_empty_documents_returns_empty_status` | PyPDFLoader returns empty → `status == "empty"` |
| `test_control_re_extracts_nist_ids` | Regex matches "AC-2", "AC-2(1)", "SI-7" |
| `test_control_re_rejects_invalid_ids` | "XX-99" does not match |
| `test_ingest_success_creates_index` | Full mock → `status == "success"`, `total_chunks > 0` |
| `test_ingest_enriches_metadata` | Verify `control_ids` and `control_family` in chunk metadata |

### 2c. Expand `test_agents.py` (+8 tests)

**File**: `backend/tests/test_agents.py`

Direct unit tests for `Orchestrator.route_and_chat()` and `route_and_chat_stream()` (not via Flask client). Mock RAGEngine, LRUCache, log_interaction.

| Test | What It Verifies |
|------|-----------------|
| `test_route_and_chat_returns_required_keys` | Response has `answer`, `sources`, `agent_name`, `agent_id` |
| `test_route_and_chat_caches_stateless_query` | Call twice with no history → cache hit on second |
| `test_route_and_chat_skips_cache_with_history` | Call with history → cache not used |
| `test_route_and_chat_logs_interaction` | `log_interaction` called with correct kwargs |
| `test_route_and_chat_stream_yields_meta_chunks_done` | SSE sequence: meta, chunks, [DONE] |
| `test_route_and_chat_stream_logs_after_completion` | `log_interaction` called after full generator consumed |
| `test_route_and_chat_llm_router_fallback` | Garbage LLM response → falls back to NIST_SPECIALIST |
| `test_route_and_chat_llm_router_exception` | LLM raises → graceful fallback |

### 2d. Expand `test_rag_engine.py` (+8 tests)

**File**: `backend/tests/test_rag_engine.py`

Mock FAISS vector store for `chat()` and `chat_stream()` full paths.

| Test | What It Verifies |
|------|-----------------|
| `test_history_to_messages_empty` | Empty list → empty list |
| `test_history_to_messages_converts_roles` | user→HumanMessage, assistant→AIMessage |
| `test_history_to_messages_ignores_unknown_roles` | system role skipped |
| `test_chat_off_topic_rejection` | L2 > 1.5 → rejection message |
| `test_chat_returns_sources_and_validation` | Working index → `sources` and `validation` in response |
| `test_chat_uses_override_prompt` | `system_prompt_override` → `_build_chain` called |
| `test_chat_stream_without_index` | No index → yields empty KB message |
| `test_chat_stream_off_topic` | L2 > 1.5 → yields rejection message |

### 2e. `test_api_blueprints.py` (new file, ~10 tests)

**File**: `backend/tests/test_api_blueprints.py`

Blueprint endpoint tests using `app_client` fixture.

| Test | What It Verifies |
|------|-----------------|
| `test_config_agents_returns_list` | GET `/api/config/agents` → JSON array with 4 entries |
| `test_config_agents_has_required_keys` | Each agent has `id`, `name`, `description`, `icon`, `details` |
| `test_config_crossmap_returns_json` | GET `/api/config/crossmap` → 200 + JSON |
| `test_health_returns_checks_object` | `checks` has `database` and `faiss_index` keys |
| `test_visitors_count_returns_counts` | `unique_visitors` and `total_visits` keys present |
| `test_interactions_stats_requires_auth` | Without auth → 401 |
| `test_interactions_stats_returns_data` | With auth → `total_interactions`, `avg_latency_ms` |
| `test_ingest_disabled_in_prod` | `DISABLE_INGEST=true` → POST `/api/ingest` returns 403 |
| `test_stream_missing_message_returns_400` | Empty message → 400 |
| `test_stream_oversized_message_returns_400` | 2001-char message → 400 |

### Verification

```bash
cd backend && ./venv/bin/python -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-fail-under=80
# Expected: ~125 tests pass, 80%+ coverage
```

---

## Phase 3: Frontend Test Setup (Vitest + RTL, ~12 tests)

### 3a. Install dependencies

**File**: `frontend/package.json`

devDependencies to add:
- `vitest`
- `@testing-library/react`
- `@testing-library/jest-dom`
- `@testing-library/user-event`
- `jsdom`
- `msw` (Mock Service Worker for API mocking)

Scripts to add:
- `"test": "vitest run"`
- `"test:watch": "vitest"`
- `"test:coverage": "vitest run --coverage"`

### 3b. Vitest configuration

**New file**: `frontend/vitest.config.ts`

- Extends existing Vite config
- `test.environment`: `jsdom`
- `test.setupFiles`: `./src/test/setup.ts`
- `test.globals`: `true`
- `test.css`: `true` (Tailwind v4 needs CSS handling)

### 3c. Test setup file

**New file**: `frontend/src/test/setup.ts`

- Import `@testing-library/jest-dom/vitest` for custom matchers
- MSW server setup for API mocking (`/api/config/agents`, `/api/config/crossmap`)

### 3d. Component tests

#### `frontend/src/components/__tests__/App.test.tsx` (~4 tests)

Wrap in `ConfigProvider` with MSW-mocked API responses.

| Test | What It Verifies |
|------|-----------------|
| `test_renders_without_crashing` | App renders, no exceptions |
| `test_renders_chat_input` | Input placeholder "Ask about NIST" present |
| `test_renders_sidebar_on_desktop` | Sidebar renders |
| `test_renders_system_ready_header` | "System Ready" text visible |

#### `frontend/src/components/__tests__/MessageBubble.test.tsx` (~5 tests)

| Test | What It Verifies |
|------|-----------------|
| `test_renders_user_message` | User icon and content visible |
| `test_renders_assistant_message_with_agent_name` | Agent badge rendered |
| `test_renders_sources_section` | "Sources" heading and items |
| `test_copy_button_visible` | Copy button exists for assistant messages |
| `test_renders_markdown_content` | Bold text → `<strong>` in output |

#### `frontend/src/components/__tests__/ConfigContext.test.tsx` (~3 tests)

| Test | What It Verifies |
|------|-----------------|
| `test_provides_agents_after_fetch` | Consumer receives agents array |
| `test_provides_crossmap_after_fetch` | Consumer receives crossmap array |
| `test_sets_error_on_fetch_failure` | 500 response → error state |

### Verification

```bash
cd frontend && npm test
# Expected: 12 tests pass
```

---

## Phase 4: E2E Tests (Playwright, ~8 tests)

### 4a. Install Playwright properly

**File**: `frontend/package.json`

devDependency: `@playwright/test`
Scripts: `"test:e2e": "playwright test"`, `"test:e2e:ui": "playwright test --ui"`

### 4b. Expand existing smoke test

**File**: `frontend/e2e/app.spec.ts`

Add assertions:
- Knowledge Base section visible in sidebar
- Quick prompt buttons visible

### 4c. Chat flow E2E

**New file**: `frontend/e2e/chat.spec.ts` (~4 tests)

Tests against real backend (degraded mode — no FAISS = "Knowledge Base is empty" response).

| Test | What It Verifies |
|------|-----------------|
| `test_quick_prompt_sends_message` | Click quick prompt → user message appears → assistant responds |
| `test_manual_input_sends_message` | Type + Enter → message sent |
| `test_clear_button_resets_chat` | Send message → Clear → messages gone, quick prompts visible |
| `test_empty_input_does_not_send` | Send button disabled when input empty |

### 4d. Sidebar E2E

**New file**: `frontend/e2e/sidebar.spec.ts` (~3 tests)

| Test | What It Verifies |
|------|-----------------|
| `test_sidebar_collapse_toggle` | Click collapse → sidebar width changes |
| `test_specialist_agents_accordion` | Click section → agent cards appear |
| `test_knowledge_base_links_exist` | 3 KB links present with correct hrefs |

### Verification

```bash
cd frontend && npx playwright test
# Expected: 9 E2E tests pass (1 expanded + 4 chat + 3 sidebar + 1 original)
```

---

## Phase 5: CI/CD Hardening

### 5a. Backend coverage gate

**File**: `.github/workflows/ci.yml` — `backend-tests` job

Change test command:
```yaml
# Before:
run: python -m pytest tests/ --tb=short -q

# After:
run: python -m pytest tests/ --tb=short -q --cov=. --cov-report=term-missing --cov-fail-under=80 --ignore=tests/test_integration.py
```

### 5b. Frontend lint + unit test in CI

**File**: `.github/workflows/ci.yml`

Add to `frontend-build` job:
```yaml
- name: Lint
  run: npm run lint

- name: Unit tests
  run: npm test
```

Or add separate `frontend-tests` job for parallel execution.

### 5c. Fix E2E CI job

**File**: `.github/workflows/ci.yml` — `e2e-tests` job

Fix backend startup:
- Set `DISABLE_INGEST=true` and no `GEMINI_API_KEY`
- Orchestrator handles missing LLM gracefully (keyword-only routing)
- RAGEngine falls back to Ollama embeddings (fails at query time, not import time)
- E2E tests designed to work with degraded backend ("Knowledge Base is empty")

### 5d. Fix docker-compose embedding model

**File**: `docker-compose.prod.yml` line 30

```yaml
# Before:
GEMINI_EMBEDDING_MODEL: models/text-embedding-004

# After:
GEMINI_EMBEDDING_MODEL: models/gemini-embedding-001
```

### Verification

Push to v03 branch, verify all CI jobs pass green.

---

## Phase 6: Cleanup

### 6a. Delete dead code

**Delete**: `frontend/src/components/ChatLayout.tsx`

225 lines, exported but never imported anywhere. Confirmed by grep: `ChatLayout` only appears in its own export declaration.

### 6b. Update Makefile

**File**: `Makefile`

```makefile
# Before:
test-backend:
	cd backend && . venv/bin/activate && python -m pytest tests/ -v

test-frontend:
	cd frontend && npm run build

# After:
test-backend:
	cd backend && . venv/bin/activate && python -m pytest tests/ -v --cov=. --cov-report=term-missing

test-frontend:
	cd frontend && npm test

test-e2e:
	cd frontend && npx playwright test
```

### Verification

```bash
make test
# Expected: both backend and frontend tests pass
```

---

## File Summary

### New Files (12)

| File | Purpose |
|------|---------|
| `backend/api/auth.py` | Extracted `require_api_key` decorator |
| `backend/tests/test_auth.py` | Auth decorator unit tests (3) |
| `backend/tests/test_visitor_tracker.py` | Visitor tracker unit tests (8) |
| `backend/tests/test_ingest.py` | Ingest pipeline unit tests (6) |
| `backend/tests/test_api_blueprints.py` | Blueprint endpoint tests (10) |
| `frontend/vitest.config.ts` | Vitest configuration |
| `frontend/src/test/setup.ts` | Test setup (jsdom, RTL matchers, MSW) |
| `frontend/src/components/__tests__/App.test.tsx` | App component tests (4) |
| `frontend/src/components/__tests__/MessageBubble.test.tsx` | MessageBubble tests (5) |
| `frontend/src/components/__tests__/ConfigContext.test.tsx` | ConfigContext tests (3) |
| `frontend/e2e/chat.spec.ts` | Chat flow E2E tests (4) |
| `frontend/e2e/sidebar.spec.ts` | Sidebar E2E tests (3) |

### Modified Files (10)

| File | Change |
|------|--------|
| `backend/tests/test_api.py` | Fix patch target `app.orchestrator` → `api.chat.orchestrator` |
| `backend/tests/test_integration.py` | Fix fixture `client` → `app_client` |
| `backend/tests/conftest.py` | Blueprint-aware patching (replace importlib.reload) |
| `backend/tests/test_agents.py` | +8 tests for route_and_chat / route_and_chat_stream |
| `backend/tests/test_rag_engine.py` | +8 tests for chat / chat_stream / _history_to_messages |
| `backend/api/chat.py` | Import `require_api_key` from `api.auth` |
| `backend/api/health.py` | Import `require_api_key` from `api.auth` |
| `backend/requirements-dev.txt` | Add `pytest-cov>=6.0` |
| `docker-compose.prod.yml` | Fix embedding model `text-embedding-004` → `gemini-embedding-001` |
| `.github/workflows/ci.yml` | Coverage gate, lint step, frontend tests, fix E2E job |

### Deleted Files (1)

| File | Reason |
|------|--------|
| `frontend/src/components/ChatLayout.tsx` | Dead code — 225 lines, zero imports |

---

## Estimated Impact

| Metric | Before | After |
|--------|--------|-------|
| Total tests | ~95 (2 broken) | ~165 (0 broken) |
| Backend coverage | Unknown (unenforced) | 80%+ (CI-enforced) |
| Frontend unit tests | 0 | 12 component tests |
| E2E tests | 1 smoke | 8+ flow tests |
| CI jobs | 4 (fragile) | 5+ (hardened) |
| Dead code | ChatLayout.tsx (225 lines) | Removed |
| DRY violations | require_api_key x2 | Extracted to auth.py |
| docker-compose config | Wrong embedding model | Fixed |

---

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Refactored conftest breaks existing test_api.py tests | Run full suite after each conftest change; 24 tests serve as regression |
| E2E tests flaky in CI (no FAISS, no LLM) | Design E2E for degraded backend; use Playwright waitFor + 2 retries |
| Vitest + Tailwind v4 CSS processing issues | Set `test.css: true`; mock CSS imports if needed |
| `pytest-cov --cov-fail-under=80` fails before new tests added | Add Phase 2 tests before enabling CI gate |
| Backend startup failure in CI E2E (missing LLM) | Orchestrator handles EnvironmentError gracefully; keyword-only routing |
