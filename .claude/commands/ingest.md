# /project:ingest — Re-embed NIST Documents

Re-ingest the NIST SP 800-53 source documents and rebuild the FAISS index.

## Warning

Changing the embedding model invalidates the existing index. Always coordinate with a full Docker release when changing `GEMINI_EMBEDDING_MODEL`.

## Steps

```bash
cd backend
export GEMINI_API_KEY=<your-key>
export GEMINI_EMBEDDING_MODEL=models/text-embedding-004

# Run ingest
./venv/bin/python ingest.py

# Verify index built
ls -lh index_kms/

# Run eval to check quality
make eval
```

## Post-Ingest Validation

1. Check `index_kms/index.faiss` and `index_kms/index.pkl` exist
2. Run `make eval` — avg_relevance_score must be ≤ previous baseline
3. Test query "What is AC-2?" manually
4. Upload new index assets to GitHub Release before deploying
