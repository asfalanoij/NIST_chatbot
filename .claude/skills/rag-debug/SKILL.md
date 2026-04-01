---
name: rag-debug
description: Auto-triggered on FAISS errors, embedding mismatch, or empty Knowledge Base results
triggers:
  - "Knowledge Base empty"
  - "FAISS"
  - "embedding mismatch"
  - "index not found"
  - "no documents"
---

# RAG Debug Skill

## When This Triggers

This skill fires when you encounter:
- "Knowledge Base empty" or zero sources returned
- FAISS load errors or missing index files
- Suspiciously high L2 scores (> 2.0) for on-topic queries
- "embedding mismatch" or dimension errors

## Diagnosis Steps

### Step 1: Check Index Files

```bash
ls -lh backend/index_kms/
# Expected: index.faiss (~5MB) and index.pkl (~1MB)
```

### Step 2: Check Embedding Model Consistency

```python
import os
print("Runtime model:", os.getenv("GEMINI_EMBEDDING_MODEL", "not set"))
# Must match what was used during ingest
# Default: models/text-embedding-004
```

### Step 3: Test Retrieval

```python
from rag_engine import RAGEngine
engine = RAGEngine()
print(f"Vectors: {engine.db.index.ntotal}")
docs = engine.db.similarity_search_with_score("What is AC-2?", k=1)
print(f"Top L2 score: {docs[0][1]:.4f}")
# Expected: < 1.0 for "What is AC-2?"
```

### Step 4: Fix

| Symptom | Fix |
|---------|-----|
| Index files missing | Re-run ingest: `./venv/bin/python ingest.py` |
| L2 > 2.0 for on-topic | Embedding model mismatch — re-ingest with correct model |
| Empty sources | L2 threshold too low — check `L2_THRESHOLD` env var |
| Dimension error | Old index from different model — delete and re-ingest |

## Prevention

Always set `GEMINI_EMBEDDING_MODEL` env var before ingest AND before starting the app.
They must be identical.
