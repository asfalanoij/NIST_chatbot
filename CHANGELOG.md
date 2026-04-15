# Changelog

All significant changes to the NIST 800-53 Chatbot are documented here.

---

## v3.0.0 — 2026-04-14

**Branch:** `v03` | **PR:** #15 | **Tag:** pending

### Zero-Hallucination RAG Engine
- **Faithfulness validation** — every LLM response is checked against retrieved source documents before delivery. Ungrounded citations (`[p.XX]`) are stripped; ungrounded control IDs are flagged.
- **Page-tolerance logic** — citations within +/-1 page of a real source page are accepted; anything else is removed.
- **Off-topic rejection** — queries with L2 distance > 1.5 from all chunks are rejected with a polite redirect instead of hallucinated answers.

### Embedding Model Upgrade
- Switched from `text-embedding-004` to `models/gemini-embedding-001` (768-dim).
- Full re-ingest of NIST SP 800-53 Rev.5 — **1,617 chunks**, 792 with structured `control_ids` metadata.
- FAISS index rebuilt and verified: "What is AC-2?" returns L2 < 1.0.

### Lean Agent Architecture
- Reduced from 7 agents to **4 specialist agents**: NIST Controls, Audit & Assessment, Risk & Impact, Compliance Mapping.
- Removed PM, QA, and DevSecOps agents — these were noise for end-user queries.
- Keyword-first routing saves 1 LLM call for ~70% of queries; LLM router handles the rest.

### Streaming & Caching
- **SSE streaming** (`POST /api/chat/stream`) — real-time token delivery with `[DONE]` sentinel.
- **LRU cache** — SHA-256 keyed by `question + agent_id`, avoids redundant LLM calls. Target >30% hit rate after warm-up.

### Interaction Logging
- Every query/response pair logged to SQLite (`interaction_log.db`) with: question hash, agent, latency, word count, citation count.
- `/api/interactions/stats` endpoint for monitoring quality metrics.
- Questions stored as SHA-256 hashes — no PII in logs.

### Testing & CI Hardening
- **140 backend tests** passing with >80% line coverage.
- New test suites: `test_visitor_tracker.py`, `test_ingest.py`, `test_api_blueprints.py`, expanded `test_agents.py` and `test_rag_engine.py`.
- **Frontend**: Vitest setup with 11 unit tests (App, ConfigContext, MessageBubble).
- **CI pipeline**: pytest with coverage gate, ESLint, frontend build verification, Bandit SAST, pip-audit dependency scan.

### Security Patches
- `langchain-core` 1.2.13 → 1.2.28 (CVE-2026-40087)
- `pypdf` 6.9.2 → 6.10.0 (CVE-2026-40260)
- Timing-safe API key comparison (`hmac.compare_digest`).
- Error responses never expose stack traces or internal paths.
- Security headers added via Flask middleware.
- Rate limiting: 10 req/min on `/api/chat`, 5 req/min on `/api/ingest`.

### UI Redesign — Right Sidebar
- Panel width: 320px → 420px for readability.
- Font sizes: 8-10px → 11-13px across all sections.
- New **"What Changed — v03"** section highlighting: zero-hallucination engine, smarter embeddings, lean agents, test coverage, security hardening.
- Increased padding and dot indicators for visual clarity.

### Infrastructure
- Pydantic v2 schemas for all LLM input/output (`backend/schemas.py`).
- Auth blueprint extracted to `backend/api/auth.py`.
- `@require_api_key` decorator on all endpoints; empty `API_KEY` = dev mode.
- Docker Compose production config updated.
- VPS deployment workflow (docker-compose, nginx, GitHub Actions CD).

---

## v2.1.0 — 2026-02-28

**Branch:** `dev` → `main` | **Tag:** `v2.1.0`

### Production Deployment
- Deployed to **Render.com** — backend (Docker + gunicorn) and frontend (static site).
- Custom domains: `80053.rudyprasetiya.com` (frontend), `80053-api.rudyprasetiya.com` (backend).
- Cloudflare DNS with CNAME records (grey cloud / DNS only) to avoid SSL 525 errors.
- `render.yaml` blueprint: web service + static site + PostgreSQL.

### Security Hardening
- Fixed information disclosure in error responses.
- Added `SECURITY.md` with vulnerability reporting policy.
- Patched pypdf CVE in dependencies.
- Rewritten README with clear UVP (Unique Value Proposition).

### Deployment Fixes
- Dockerfile downloads FAISS index from GitHub Release at build time (not in git).
- Fixed `VITE_API_URL` environment variable for frontend → backend connectivity.
- Removed `customDomains` from render.yaml (configured in Render dashboard instead).
- Free tier configuration for backend web service.
- Render deployment guide with Cloudflare DNS notes.

---

## v2.0.0 — 2026-02-27

**Branch:** `dev` → `main` | **PR:** #2 | **Tag:** `v2.0.0`

### Production-Ready Backend
- Flask application restructured into blueprint-based architecture.
- **gunicorn** with Procfile (2 workers, 120s timeout).
- All `print()` statements replaced with `logging` module.
- 16 packages pinned in `requirements.txt`.

### RAG Pipeline
- **MMR retrieval** (k=5, fetch_k=20) — Maximal Marginal Relevance for diverse results.
- L2 score threshold > 1.5 rejects off-topic queries.
- Chat history support via `MessagesPlaceholder`.
- Cached default chain + router chain (not rebuilt per request).
- **1,540 vectors** in FAISS index, uploaded to GitHub Release v2.0.0.

### Multi-Agent Orchestration
- 7 specialist agents: NIST Controls, Audit, Risk, Compliance, PM, QA, DevSecOps.
- Keyword-first routing with LLM fallback.
- Each agent has a tailored system prompt for its domain.

### Database & Monitoring
- PostgreSQL visitor tracker (`DATABASE_URL`) with SQLite fallback.
- `flask-limiter`: 10 req/min chat, 5 req/min ingest.
- `DISABLE_INGEST=true` in production.
- Enhanced `/api/health`: checks DB + FAISS index status.

### Frontend
- React 19 + Vite 7 + Tailwind v4.
- Three-panel layout: left sidebar (agents, knowledge base) + chat + right sidebar (insights).
- Quick prompt buttons for common NIST queries.
- Source citations displayed with page references.
- `VITE_API_URL` env var via `frontend/src/config.ts`.

### CI/CD
- GitHub Actions: pytest + frontend build on push/PR.
- 58 tests passing at release.
- GitHub ruleset "prudent" on main: requires PR + signed commits.

---

## v1.0.0 — 2025-08-18

**Branch:** `main` | **Tag:** none

### Initial MVP
- RAG chatbot for NIST SP 800-53 Rev.5 using FAISS vector search.
- Basic Flask backend with LangChain integration.
- PDF ingestion pipeline with recursive text splitting.
- Ollama as default LLM backend (local inference).
- Single-page frontend prototype.
- Baseline chunking: recursive character splitter with NIST-aware separators (`\nFamily:`, `\nControl:`).
