---
name: backend-feature-development-and-hardening
description: Workflow command scaffold for backend-feature-development-and-hardening in NIST_chatbot.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /backend-feature-development-and-hardening

Use this workflow when working on **backend-feature-development-and-hardening** in `NIST_chatbot`.

## Goal

Implements new backend features or hardening, including logic, tests, and requirements updates.

## Common Files

- `backend/*.py`
- `backend/requirements.txt`
- `backend/requirements-dev.txt`
- `backend/tests/*.py`
- `.gitignore`
- `Makefile`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit or add backend Python files for feature or fix (e.g., backend/agents.py, backend/app.py, backend/visitor_tracker.py, backend/rag_engine.py, etc.)
- Update requirements.txt and/or requirements-dev.txt if dependencies change
- Add or update test files in backend/tests/
- Update .gitignore or Makefile if needed

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.