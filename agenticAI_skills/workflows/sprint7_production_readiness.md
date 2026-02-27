# Sprint 7: Production Readiness — Design Document

## Goal
Harden the NIST 800-53 chatbot for deployment as a public SaaS MVP on Render.

## Target
- Platform: Render (PaaS)
- Domain: nist80053.rudyprasetiya.com
- Scale: <100 users (MVP)
- LLM: Gemini 2.0 Flash (cloud-only in production)

## Understanding Summary
- **What**: Production-harden existing Flask + React chatbot
- **Why**: Take working prototype (Sprint 6, 38 tests, 7 agents) to internet-facing SaaS
- **Who**: Public users, compliance/security professionals
- **Constraints**: Single-server PaaS, budget-conscious, no Kubernetes

## Non-Goals (YAGNI)
- Multi-tenancy / user isolation
- Billing / payment integration
- SSO / OAuth
- Horizontal scaling / queues
- Kubernetes

## Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Keep Flask (no FastAPI) | 38 tests pass, YAGNI |
| 2 | Incremental hardening | PaaS handles TLS/routing |
| 3 | PostgreSQL for visitors | Render ephemeral FS loses SQLite |
| 4 | DATABASE_URL + SQLite fallback | Preserves local dev |
| 5 | gunicorn WSGI | Industry standard |
| 6 | Pre-baked FAISS in Docker | Deterministic, no runtime ingest |
| 7 | Rate limit: 10/min chat | Gemini cost protection |
| 8 | JSON logging in prod | Render log drain compatible |
| 9 | Separate frontend static site | CDN-friendly |
| 10 | GitHub Actions CI only | Render auto-deploys |
| 11 | Custom domain | Professional branding |
| 12 | Gemini-only in prod | Ollama can't run on PaaS |

## Implementation Phases

### Phase 1 — Backend Hardening
1. Replace 8 print() → logging with JSON/text toggle
2. Add gunicorn to requirements.txt + Procfile
3. Migrate visitor_tracker.py to PostgreSQL with SQLite fallback
4. Add flask-limiter (10/min chat, 5/min ingest)
5. Enhance /api/health → check DB + FAISS readiness

### Phase 2 — Deployment Config
6. Create Dockerfile (Python 3.12, gunicorn, baked FAISS index)
7. Create render.yaml blueprint (web service + postgres + static site)
8. Add CORS_ORIGINS for production domain
9. Disable /api/ingest in production (env toggle)

### Phase 3 — CI + Quality
10. Create .github/workflows/ci.yml (pytest + frontend build + lint)
11. Add .dockerignore
12. Update README with deployment instructions

### Phase 4 — Ship
13. Re-ingest documents with Gemini embeddings
14. Push via PR → merge → Render auto-deploys
15. Configure custom domain + TLS on Render
16. Git tag v2.0.0

## Assumptions
- Gemini API key will be set as env var on Render
- FAISS index rebuilt locally, committed to repo
- Frontend build served from Render Static Site
- PostgreSQL provisioned via Render managed add-on
