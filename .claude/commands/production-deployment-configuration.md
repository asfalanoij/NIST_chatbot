---
name: production-deployment-configuration
description: Workflow command scaffold for production-deployment-configuration in NIST_chatbot.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /production-deployment-configuration

Use this workflow when working on **production-deployment-configuration** in `NIST_chatbot`.

## Goal

Updates deployment configuration for production, including Render, Docker, and GitHub Actions CI/CD.

## Common Files

- `render.yaml`
- `backend/Dockerfile`
- `backend/Procfile`
- `.github/workflows/ci.yml`
- `frontend/src/config.ts`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit render.yaml to update deployment settings (e.g., custom domains, API URLs, free tier).
- Edit or add backend/Dockerfile and backend/Procfile for containerization and WSGI setup.
- Update .github/workflows/ci.yml for CI/CD pipeline changes.
- Update frontend/src/config.ts or similar for API base URLs.
- Commit and merge changes to main or production branch.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.