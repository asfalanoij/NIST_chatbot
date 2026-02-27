# NIST 800-53 Compliance Chatbot v02

**An agentic, RAG-powered chatbot that makes NIST RMF and SP 800-53 accessible.**

Built to solve a real pain point: organizations struggle to understand, implement, and audit NIST security controls. This chatbot routes your question to the right specialist agent and answers using your actual compliance documents.

> Privacy-first. Runs 100% locally via Ollama. Optional Gemini cloud fallback.

**Author**: [Rudy Prasetiya](https://rudyprasetiya.com)

---

## Architecture

```
User Question
     |
     v
 [Orchestrator] --LLM routing + keyword fallback-->
     |
     +--> NIST Controls Specialist    (800-53 Rev.5, RMF lifecycle)
     +--> Audit & Assessment Agent    (evidence, test procedures, POA&Ms)
     +--> Risk & Impact Agent         (FIPS 199, CIA triad, tailoring)
     +--> Compliance Mapping Agent    (FedRAMP, CMMC, ISO 27001, SOC 2)
     +--> Product Manager Agent       (roadmaps, prioritization, business value)
     |
     v
 [RAG Engine] --> FAISS vector store --> LLM (Ollama/Gemini) --> Answer + Citations
```

| Layer | Stack |
|-------|-------|
| Frontend | React 19, Vite 7, TypeScript, Tailwind CSS v4, Lucide Icons |
| Backend | Python 3.12, Flask, LangChain, FAISS |
| LLM | Ollama (llama3, local) or Gemini 2.0 Flash (cloud fallback) |
| Retrieval | PDF ingestion, recursive chunking (2000 tokens, 300 overlap), NIST-aware separators |

## Key Features

- **5 Specialist Runtime Agents** — Automatic routing to the right expert based on your question
- **8 Build-Time Agents** — QA inspection, security scanning, maturity tracking, and more via `./antigravity.sh`
- **RAG with Citations** — Every answer cites the source document and page number
- **Gemini Fallback** — Automatically uses Google Gemini if `GEMINI_API_KEY` is set, otherwise Ollama
- **Visitor Tracking** — SQLite-based visitor counter with `/api/visitors/count` endpoint
- **NIST-Aware Chunking** — Splitting strategy preserves control family context
- **Security Hardened** — CORS origin-locked, env-based config, no hardcoded secrets
- **26 Backend Tests** — Full pytest suite for API, agents, and RAG engine
- **Quick-Start Prompts** — Pre-built queries for common compliance questions

## Quick Start

### Prerequisites

- Node.js 18+ & npm
- Python 3.10+
- [Ollama](https://ollama.com) installed and running

```bash
# Pull an LLM model
ollama pull llama3
ollama serve
```

### Setup & Run

```bash
# 1. Copy environment config
cp .env.example .env
# Edit .env — add GEMINI_API_KEY if you want cloud fallback

# 2. Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Ingest your NIST documents (place PDFs in docs/)
python ingest.py

# 4. Start backend (port 5050)
python app.py

# 5. Frontend (new terminal)
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

Or use the Makefile:

```bash
make setup         # Install both backend & frontend deps
make ingest        # Process PDFs into vector index
make start-backend
make start-frontend
make test          # Run all tests
make qa            # Run 16-point quality inspection
make scan          # Run security scan
make maturity      # Check project maturity %
```

## Build Agents (AntiGravity System)

8 build-time agents for development quality assurance:

```bash
./agenticAI_skills/antigravity.sh help     # List all agents
./agenticAI_skills/antigravity.sh qa inspect         # 16-point quality check
./agenticAI_skills/antigravity.sh devsecops scan     # Security scan
./agenticAI_skills/antigravity.sh nist-expert validate  # RAG coverage check
./agenticAI_skills/antigravity.sh data-scientist profile  # Embedding stats
./agenticAI_skills/antigravity.sh pm maturity        # Project maturity %
./agenticAI_skills/antigravity.sh e2e-test run       # Run all tests
./agenticAI_skills/antigravity.sh context-optimizer report  # Token analysis
./agenticAI_skills/antigravity.sh visitor-tracker status    # Visitor health
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check + active LLM backend |
| `/api/chat` | POST | Route question to specialist agent |
| `/api/ingest` | POST | Trigger PDF ingestion |
| `/api/visitors/count` | GET | Unique visitors & total visits |

## Gemini Fallback

To use Google Gemini instead of local Ollama:

1. Get an API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Add to your `.env`: `GEMINI_API_KEY=your_key_here`
3. Restart the backend — it auto-detects and uses Gemini

## Testing

```bash
# Backend tests
cd backend && source venv/bin/activate && pytest tests/ -v

# Frontend build check
cd frontend && npm run build

# Full test suite
make test
```

## Knowledge Base

Place PDF files in `docs/` at the project root:

| Document | Purpose |
|----------|---------|
| `nist_80053r5.pdf` | SP 800-53 Rev.5 control catalog |
| `nist_1362.pdf` | NIST SP 1362 supplemental guidance |
| `fedramp.pdf` | FedRAMP authorization requirements |
| `incidentresponseforwindows.pdf` | IR procedures reference |

---

**License**: MIT
