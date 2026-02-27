# Context Map — NIST 800-53 Chatbot v02
> Token-optimized project index. ~80 lines.

## Directory Structure
```
NIST_chatbot_v02/
├── backend/
│   ├── app.py              (100 lines)  Flask API + @require_api_key auth
│   ├── rag_engine.py       (120 lines)  RAG + get_llm() + get_embeddings() fallback
│   ├── agents.py           (175 lines)  7 runtime agents + Orchestrator + keyword routing
│   ├── ingest.py           (64 lines)   PDF → chunks → FAISS via get_embeddings()
│   ├── visitor_tracker.py  (48 lines)   SQLite: track_visit(), get_visitor_counts()
│   ├── requirements.txt    (11 deps)    flask, langchain, faiss-cpu, pytest, langchain-google-genai
│   └── tests/
│       ├── conftest.py     Flask test client + Orchestrator mock (fixed)
│       ├── test_api.py     13 tests: health, chat, validation, auth (6 new)
│       ├── test_agents.py  17 tests: definitions, keywords, routing (QA + DevSecOps added)
│       └── test_rag_engine.py  8 tests: LLM fallback, embeddings fallback, init, empty index
├── frontend/
│   └── src/components/
│       ├── ChatLayout.tsx  (215 lines) Main UI, sidebar, X-API-Key header, visitor badge
│       └── MessageBubble.tsx (77 lines) Markdown rendering + source citations
├── agenticAI_skills/
│   ├── antigravity.sh      Dispatcher: ./antigravity.sh <agent> <skill> (13 agents)
│   ├── utils.sh            Colors, logging, score tracking (bash 3.2 compatible)
│   ├── qa/agent.sh         16-point inspection
│   ├── devsecops/agent.sh  10-point security scan
│   ├── nist-expert/agent.sh  10-point RAG/NIST validation
│   ├── data-scientist/agent.sh  Embedding & chunk profile
│   ├── pm/agent.sh         Weighted maturity % (11 indicators)
│   ├── e2e-test/agent.sh   Backend tests + frontend build + health
│   ├── context-optimizer/agent.sh  Token count analysis
│   ├── visitor-tracker/agent.sh  Visitor tracking health
│   ├── api-auth/agent.sh   8-point auth verification (NEW)
│   ├── api-loadtest/agent.sh  Endpoint stress testing (NEW)
│   ├── rag-evaluator/agent.sh  Retrieval quality + 5 test queries (NEW)
│   ├── chat-export/agent.sh  6-point export readiness (NEW)
│   ├── cicd/agent.sh       10-point CI/CD pipeline check (NEW)
│   ├── MEMORY.md           Layer 1: auto-loaded session context
│   ├── context_map.md      Layer 2: this file
│   └── workflows/          Layer 3: on-demand plans & logs
├── docs/                   4 PDFs: 800-53r5, 1362, FedRAMP, IR
├── index_kms/              FAISS index (needs rebuild after embedding change)
├── .env.example            All config keys (API_KEY, GEMINI_EMBEDDING_MODEL added)
├── .gitignore              Covers .env, *.db, .logs/, venv/, node_modules/
├── Makefile                setup, start-*, ingest, test-*, qa, scan, maturity, auth, loadtest, rag-eval, cicd
└── README.md               Project docs (137 lines)
```

## Endpoint Matrix
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/health` | GET | None | Status + LLM backend name |
| `/api/chat` | POST | X-API-Key | Route → Agent → RAG → Answer + Sources |
| `/api/ingest` | POST | X-API-Key | Trigger PDF ingestion |
| `/api/visitors/count` | GET | None | `{unique_visitors, total_visits}` |

## Data Flow
```
User → ChatLayout.tsx → POST /api/chat (+ X-API-Key header)
  → @require_api_key check → @before_request (track_visit)
  → Orchestrator.route_and_chat() → LLM route OR keyword fallback
  → Agent persona selected → RAGEngine.chat() → FAISS similarity_search(k=5)
  → LLM (Ollama/Gemini) → Answer + Sources → JSON response → MessageBubble.tsx
```

## Embedding Flow
```
get_embeddings() → GEMINI_API_KEY set? → GoogleGenerativeAIEmbeddings (3072-dim)
                 → No key?            → OllamaEmbeddings (768-dim)
Both ingest.py and rag_engine.py call get_embeddings() → always in sync
```
