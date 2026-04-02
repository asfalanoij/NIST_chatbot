---
name: ci-cd-pipeline-update-or-deployment-workflow
description: Workflow command scaffold for ci-cd-pipeline-update-or-deployment-workflow in NIST_chatbot.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /ci-cd-pipeline-update-or-deployment-workflow

Use this workflow when working on **ci-cd-pipeline-update-or-deployment-workflow** in `NIST_chatbot`.

## Goal

Adds or updates CI/CD pipeline files and deployment configuration for new environments or hardening.

## Common Files

- `.github/workflows/ci.yml`
- `.github/workflows/deploy.yml`
- `docker-compose.prod.yml`
- `nginx/nist-chatbot.conf`
- `render.yaml`
- `backend/Dockerfile`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit or add .github/workflows/*.yml for CI/CD
- Edit or add deployment files (docker-compose.prod.yml, render.yaml, nginx configs, backend/Dockerfile, backend/Procfile, etc.)
- Update .gitignore if new secrets/configs are introduced
- Commit all changes together

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.