---
name: backend-feature-or-refactor-with-tests
description: Workflow command scaffold for backend-feature-or-refactor-with-tests in NIST_chatbot.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /backend-feature-or-refactor-with-tests

Use this workflow when working on **backend-feature-or-refactor-with-tests** in `NIST_chatbot`.

## Goal

Implements or refactors backend features, always updating core backend modules and corresponding tests.

## Common Files

- `backend/agents.py`
- `backend/app.py`
- `backend/rag_engine.py`
- `backend/visitor_tracker.py`
- `backend/crossmap.py`
- `backend/tests/test_agents.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit or add backend Python modules (e.g., agents.py, rag_engine.py, visitor_tracker.py, crossmap.py)
- Update or add corresponding test files in backend/tests/
- Update requirements.txt or requirements-dev.txt if dependencies change

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.