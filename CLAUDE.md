# NIST 800-53 Chatbot — v03

## MISSION (read first, always)

Build and maintain the **FASTEST** and **MOST RELEVANT** NIST 800-53 chatbot.
Every change must be measured against: retrieval accuracy, response latency, citation correctness.

## NEVER DO (without explicit user confirmation)

- Add features unrelated to NIST 800-53 compliance queries
- Change the `/api/chat` response schema keys (`answer`, `sources`, `agent_name`, `agent_id`)
- Deploy without running `make test-backend` (38+ tests must pass)
- Change embedding model without coordinating a full re-ingest + Docker release
- Raise the L2 rejection threshold above 2.0

## ALWAYS DO

- Load `@rag-engineer` skill before touching retrieval code
- Run `nist-validator` agent after changing any system prompt
- Run `code-reviewer` agent after every backend file change
- Check interaction stats after any retrieval change to verify quality didn't regress
- Keep answers ≤ 200 words with `[p.XX]` citations

## Stack

| Layer | Tech |
|-------|------|
| Backend | Flask + LangChain + FAISS |
| LLM | Gemini Flash (GEMINI_API_KEY) / Ollama fallback |
| Embeddings | models/gemini-embedding-001 (768-dim) after Phase 5 |
| Frontend | React 19 + Vite 7 + Tailwind v4 |
| DB | PostgreSQL (prod) / SQLite fallback |
| Hosting | Render.com |

## Commands

| Command | Action |
|---------|--------|
| `make test-backend` | Run pytest (38+ tests must pass) |
| `make eval` | Run rag-evaluator + print interaction stats |
| `/project:qa` | 16-point QA agent |
| `/project:ingest` | Re-embed NIST docs |
| `/project:deploy` | qa + scan + test + push |

## Architecture Guardrails

- Embedding model at ingest MUST match query time — #1 failure mode
- Cache key: `sha256(question.lower() + ":" + agent_id)[:16]`
- Interaction log: `backend/interaction_log.db` (gitignored, SQLite)
- FAISS index: `backend/index_kms/` (gitignored, downloaded in Docker)
- venv: `backend/venv/` — always use `backend/venv/bin/python` for tests

## Quality Metrics (North Star)

| Metric | Target |
|--------|--------|
| Retrieval L2 score (top chunk) | < 1.0 for on-topic queries |
| P50 latency | < 2s |
| P95 latency | < 5s |
| Answer word count | ≤ 200 words (100%) |
| Citation `[p.XX]` present | ≥ 95% of answers |
| Control IDs bolded `**AC-2**` | 100% when controls mentioned |
| Cache hit rate | > 30% after warm-up |
| Test coverage | 80%+ lines, 0 failures |
