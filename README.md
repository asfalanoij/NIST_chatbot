# NIST 800-53 Intelligence Platform

> **Stop searching 1,189 controls manually. Ask the right specialist instead.**

Live demo → **[80053.rudyprasetiya.com](https://80053.rudyprasetiya.com)**

---

## The Problem

Organizations managing federal systems or government contracts must demonstrate NIST 800-53 compliance — or risk losing their ATO. 
However, the control catalog is 400+ pages. 
PAIN POINT: Knowing *which controls apply*, *how to implement them*, and *what evidence to collect* takes hours of expert research per question.

Most teams either hire expensive consultants or produce compliance artifacts that might not survive audit scrutiny.

## What This Does

An agentic RAG system that routes your compliance question to the right specialist and answers from your actual source documents — with citations.

```
Your question
     │
     ▼
[Orchestrator] ── keyword routing + LLM fallback ──────────────────────┐
     │                                                                   │
     ├── NIST Controls Specialist    SP 800-53 Rev.5, RMF lifecycle      │
     ├── Audit & Assessment Agent    Evidence, POA&Ms, test procedures   │
     ├── Risk & Impact Agent         FIPS 199, CIA triad, tailoring      │
     ├── Compliance Mapping Agent    FedRAMP, CMMC, ISO 27001, SOC 2     │
     ├── Project Manager Agent       Roadmaps, prioritization            │
     ├── QA Agent                    Test plans, validation              │
     └── DevSecOps Agent             Pipeline security, hardening        │
                                                                         │
     ▼                                                                   │
[RAG Engine] → FAISS (1,540 vectors) → Gemini 2.0 Flash ◄──────────────┘
     │
     ▼
Answer + source document + page number
```

**Cross-framework mapping** — 30 NIST controls mapped to ISO 27001, CSF 2.0, and ISO 27005 with Sankey diagram export.

---

## Why It's Different

| | Typical chatbot | This platform |
|---|---|---|
| Knows *your* documents | ✗ Generic training data | ✓ RAG from your PDFs |
| Right expert per question | ✗ One generic model | ✓ 7 routed specialist agents |
| Cites the source | ✗ Hallucinated references | ✓ Doc + page number |
| Cross-framework aware | ✗ NIST only | ✓ ISO 27001, CSF 2.0, CMMC |
| Audit-ready output | ✗ Summaries | ✓ Evidence artifacts, POA&Ms |

---

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite 7, TypeScript, Tailwind CSS v4 |
| Backend | Python 3.12, Flask, LangChain, FAISS |
| LLM | Gemini 2.0 Flash (prod) · Ollama local (dev) |
| Retrieval | MMR search, 2000-token NIST-aware chunking, L2 score filtering |
| Infra | Docker, gunicorn, PostgreSQL, Render, rate-limited API |

---

## Quick Start

### Prerequisites
- Node.js 18+ & npm
- Python 3.10+
- [Ollama](https://ollama.com) (local dev) or Gemini API key (recommended)

```bash
# Clone
git clone https://github.com/asfalanoij/NIST_chatbot
cd NIST_chatbot

# Environment
cp .env.example .env
# Add GEMINI_API_KEY to .env for best results

# Backend
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Ingest your NIST documents (place PDFs in docs/)
python ingest.py

# Start backend (port 5050)
python app.py

# Frontend (new terminal)
cd frontend && npm install && npm run dev
# Open http://localhost:5173
```

Or with Make:
```bash
make setup && make ingest && make start-backend
# new terminal:
make start-frontend
```

---

## Knowledge Base

Place PDFs in `docs/` at the project root:

| File | Content |
|------|---------|
| `nist_80053r5.pdf` | SP 800-53 Rev.5 — full control catalog |
| `nist_1362.pdf` | NIST SP 1362 — supplemental guidance |
| `fedramp.pdf` | FedRAMP authorization requirements |
| `incidentresponseforwindows.pdf` | IR procedures reference |

---

## API Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/health` | GET | — | Status, LLM backend, DB check |
| `/api/chat` | POST | API key | Route question to specialist agent |
| `/api/visitors/count` | GET | — | Visitor statistics |
| `/api/crossmap` | GET | — | NIST → ISO 27001 / CSF 2.0 / ISO 27005 |
| `/api/crossmap/stats` | GET | — | Coverage statistics |
| `/api/crossmap/sankey` | GET | — | Download Sankey CSV |
| `/api/ingest` | POST | API key | Trigger PDF ingestion (disabled in prod) |

**Chat request:**
```json
POST /api/chat
Headers: X-API-Key: <key>

{
  "message": "What evidence do I need for AC-2 assessment?",
  "history": []
}
```

---

## Build Agents (AntiGravity System)

13 bash agents for development quality assurance:

```bash
./agenticAI_skills/antigravity.sh help              # List all agents
./agenticAI_skills/antigravity.sh qa inspect        # 16-point quality check
./agenticAI_skills/antigravity.sh devsecops scan    # Security scan
./agenticAI_skills/antigravity.sh nist-expert validate  # RAG coverage check
./agenticAI_skills/antigravity.sh pm maturity       # Project maturity %
./agenticAI_skills/antigravity.sh e2e-test run      # Full test suite
```

---

## Deployment (Render)

One-command deploy via Blueprint:

1. Fork the repo → connect to [Render](https://render.com) → select **Blueprint** → point to this repo
2. Set `GEMINI_API_KEY` when prompted
3. All 3 services (API, frontend, PostgreSQL) deploy automatically from `render.yaml`

Custom domain, CORS, rate limiting, and gunicorn are pre-configured. See [`agenticAI_skills/workflows/render_deployment_guide.md`](agenticAI_skills/workflows/render_deployment_guide.md) for DNS setup.

---

## Testing

```bash
cd backend && source venv/bin/activate
pytest tests/ -v          # 58 tests

cd frontend
npm run build             # Type-check + build
```

---

## Security

- CORS locked to configured origins (`CORS_ORIGINS` env var)
- API key authentication on write endpoints (`X-API-Key` header)
- Rate limiting: 10 req/min chat, 5 req/min ingest
- Ingestion disabled in production (`DISABLE_INGEST=true`)
- No secrets in code — all config via environment variables
- Dependencies pinned; CVE monitoring via GitHub Dependabot

---

**Author**: [Rudy Prasetiya](https://rudyprasetiya.com) · **License**: MIT
