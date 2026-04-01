---
name: backend-feature-development-and-hardening
description: Workflow command scaffold for backend-feature-development-and-hardening in NIST_chatbot.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /backend-feature-development-and-hardening

Use this workflow when working on **backend-feature-development-and-hardening** in `NIST_chatbot`.

## Goal

Implements or hardens backend features, often including new modules, updating core backend files, and adding/expanding tests.

## Common Files

- `backend/agents.py`
- `backend/app.py`
- `backend/rag_engine.py`
- `backend/interaction_log.py`
- `backend/cache.py`
- `backend/crossmap.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Implement or update backend logic in one or more of: backend/agents.py, backend/app.py, backend/rag_engine.py, backend/interaction_log.py, backend/cache.py, backend/crossmap.py, etc.
- Update or add new tests in backend/tests/ (e.g., test_agents.py, test_api.py, test_cache.py, test_crossmap.py, test_schemas.py, etc.)
- Update backend/requirements.txt and/or backend/requirements-dev.txt if dependencies change.
- Update or add supporting files (e.g., schemas.py, visitor_tracker.py, Dockerfile, Procfile) as needed.
- If relevant, update .github/workflows/ci.yml for CI changes.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.