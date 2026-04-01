# RAG Quality Standards

## Retrieval

- MMR k=5, fetch_k=20 is the baseline — do not reduce k without measuring
- L2 threshold = 1.5 rejects off-topic queries — do not raise above 2.0
- Re-index after ANY change to chunk_size, chunk_overlap, or embedding model
- Run `/project:eval` after re-index to verify no quality regression

## Chunking

- chunk_size=2000, overlap=300 are tuned for NIST SP 800-53 document structure
- Separators priority: `\nFamily:` > `\nControl:` > `\n\n` > `\n` > space
- Do not change separators without consulting `@rag-engineer` skill

## Embeddings

- Current model: `models/text-embedding-004` (768-dim) after Phase 5
- The embedding model used at ingest MUST match the model used at query time
- This is the #1 failure mode — always check `GEMINI_EMBEDDING_MODEL` env var
- Env var `GEMINI_EMBEDDING_MODEL` must be set consistently in both ingest and app runtime

## Quality Gates

Before merging any retrieval change:
1. Run `make eval` and confirm avg_relevance_score ≤ current baseline
2. Manually test: "What is AC-2?" — L2 score must be < 1.0
3. Manually test: "What is the weather?" — must be rejected (L2 > 1.5)
4. All 38+ pytest tests must pass
