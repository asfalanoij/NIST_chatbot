---
name: backend-feature-development-with-tests
description: Workflow command scaffold for backend-feature-development-with-tests in NIST_chatbot.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /backend-feature-development-with-tests

Use this workflow when working on **backend-feature-development-with-tests** in `NIST_chatbot`.

## Goal

Implements new backend features or modules, always accompanied by new or updated tests.

## Common Files

- `backend/agents.py`
- `backend/app.py`
- `backend/rag_engine.py`
- `backend/schemas.py`
- `backend/cache.py`
- `backend/interaction_log.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Create or update backend implementation files (e.g., agents.py, app.py, rag_engine.py, schemas.py, cache.py, interaction_log.py).
- Add or update corresponding test files in backend/tests/ (e.g., test_agents.py, test_api.py, test_cache.py, test_interaction_log.py, test_schemas.py).
- Update Makefile or requirements if needed.
- Update .gitignore if new artifacts are generated.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.