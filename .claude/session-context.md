## NIST Chatbot v03 — Session Context

**Mission:** ULTRA RELEVANT AND FAST NIST 800-53 chatbot. Every change = better retrieval OR faster response.

**Current phase:**
- [x] Phase 00: Interaction logging + .claude/ structure
- [x] Phase 1:  Routing fix (replace ChatOllama router with Gemini Flash)
- [x] Phase 2:  Pydantic schemas + word-limit validator
- [x] Phase 3:  LRU cache + interaction logging wired
- [x] Phase 4:  SSE streaming endpoint
- [x] Phase 5:  Embedding swap (text-embedding-004) + re-ingest

**Key architectural constraints:**
- Embedding model at ingest MUST match query time — #1 failure mode
- Never change /api/chat response keys (frontend depends on: answer, sources, agent_name, agent_id)
- Always run `make test-backend` (38+ tests) before any commit
- Interaction log DB at backend/interaction_log.db — gitignored

**Load these skills BEFORE touching these files:**
| File(s) | Load skill first |
|---------|-----------------|
| rag_engine.py, ingest.py | @rag-engineer |
| agents.py (prompts/routing) | @langchain-architecture |
| embedding model change | @embedding-strategies |
| cache.py, LRU | @prompt-caching |
| interaction_log.py, stats | @llm-evaluation |
| any new endpoint | @api-security-best-practices |

**Run these agents AFTER touching these files:**
| Changed | Run agent |
|---------|-----------|
| Any system prompt | nist-validator |
| FAISS index / retrieval | rag-reviewer |
| Any backend file | code-reviewer |
