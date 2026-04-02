---
name: backend-feature-development-and-hardening
description: Workflow command scaffold for backend-feature-development-and-hardening in NIST_chatbot.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /backend-feature-development-and-hardening

Use this workflow when working on **backend-feature-development-and-hardening** in `NIST_chatbot`.

## Goal

Implements new backend features or hardening, including code, tests, and requirements updates.

## Common Files

- `backend/app.py`
- `backend/agents.py`
- `backend/visitor_tracker.py`
- `backend/cache.py`
- `backend/interaction_log.py`
- `backend/rag_engine.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit or add backend Python modules (e.g., backend/app.py, backend/agents.py, backend/visitor_tracker.py, etc.)
- Update or add tests in backend/tests/ (e.g., test_api.py, test_agents.py, etc.)
- Update backend/requirements.txt and/or backend/requirements-dev.txt if dependencies change
- Optionally update Makefile or .gitignore
- Commit all changes together

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.