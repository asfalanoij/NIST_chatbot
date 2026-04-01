```markdown
# NIST_chatbot Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill provides a comprehensive guide to the development, maintenance, and deployment patterns used in the NIST_chatbot Python codebase. It covers coding conventions, common workflows (feature development, security patching, deployment, documentation, and repo cleanup), and testing practices. Use this as a reference for contributing effectively and consistently to the project.

## Coding Conventions

**File Naming**
- Use `camelCase` for file names.
  - Example: `interactionLog.py`, `ragEngine.py`

**Import Style**
- Use relative imports within modules.
  - Example:
    ```python
    from .cache import Cache
    from .agents import Agent
    ```

**Export Style**
- Default export style is used (i.e., no explicit `__all__` unless needed).

**Commit Patterns**
- Mixed commit types: `fix`, `feat`, `chore`, `docs`, `security`
- Commit messages are concise, average length ~54 characters.
  - Example: `fix: update cache logic for expired sessions`

## Workflows

### Backend Feature Development and Hardening
**Trigger:** When adding or improving backend features (e.g., new agent, cache, logging, security, or SSE endpoint).
**Command:** `/feature-backend`

1. Implement or update backend logic in files such as:
    - `backend/agents.py`
    - `backend/app.py`
    - `backend/rag_engine.py`
    - `backend/interaction_log.py`
    - `backend/cache.py`
    - `backend/crossmap.py`
2. Update or add tests in `backend/tests/` (e.g., `test_agents.py`, `test_api.py`).
3. Update `backend/requirements.txt` and/or `backend/requirements-dev.txt` if dependencies change.
4. Update or add supporting files (e.g., `schemas.py`, `visitor_tracker.py`, `Dockerfile`, `Procfile`) as needed.
5. If relevant, update `.github/workflows/ci.yml` for CI changes.
6. Commit all changes together.

**Example:**
```python
# backend/agents.py
class NewAgent(Agent):
    def respond(self, input):
        # New agent logic here
        pass
```

---

### Security Hardening and CVE Patching
**Trigger:** When patching vulnerabilities, adding security headers, updating dependencies for CVEs, or updating security docs/tests.
**Command:** `/security-patch`

1. Upgrade vulnerable dependencies in `backend/requirements.txt` (and sometimes `requirements-dev.txt`).
2. Update `backend/app.py` to add/adjust security headers, error handling, or authentication.
3. Add or update tests in `backend/tests/test_api.py` (or other relevant tests) to cover security cases.
4. Update `.github/workflows/ci.yml` to add or modify security scanning steps (e.g., bandit, pip-audit).
5. Optionally add or update `SECURITY.md` or `README.md` for security policy/documentation.
6. Commit all changes together.

**Example:**
```python
# backend/app.py
from flask import Flask
app = Flask(__name__)

@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
```

---

### Deployment Config Update
**Trigger:** When updating deployment settings, domains, or environment variables for production or staging.
**Command:** `/deploy-config`

1. Edit `render.yaml` to update deployment settings (domains, env vars, service tier, etc.).
2. Edit or add `backend/Dockerfile` or `backend/Procfile` if backend deployment changes are needed.
3. Optionally update frontend or documentation files if API URLs or keys change.
4. Commit all changes together.

**Example:**
```yaml
# render.yaml
services:
  - type: web
    env: python
    name: nist-chatbot-backend
    envVars:
      - key: API_KEY
        value: your-api-key
```

---

### Documentation and Guides Update
**Trigger:** When adding or updating documentation, guides, or compliance policies.
**Command:** `/docs-update`

1. Edit or add markdown files such as `README.md`, `SECURITY.md`, `agenticAI_skills/workflows/*.md`, `CLAUDE.md`, etc.
2. Commit documentation changes (sometimes with co-authors).

**Example:**
```markdown
# New Feature Guide

This document explains how to add a new agent to the backend...
```

---

### Repo Cleanup and Legacy Removal
**Trigger:** When removing obsolete, legacy, or large files/directories to keep the repo clean.
**Command:** `/repo-cleanup`

1. Delete legacy directories (e.g., `legacy/`, `rag-mvp/`, `inspo_CSS_chatbot_app/`).
2. Delete root-level screenshots, notebooks, or duplicate files (e.g., `requirements.txt`, `notes.txt`).
3. Update `.gitignore` if needed.
4. Commit all removals together.

**Example:**
```bash
rm -rf legacy/ rag-mvp/ inspo_CSS_chatbot_app/
rm *.png *.ipynb notes.txt
```

---

## Testing Patterns

- **Framework:** Unknown (no explicit framework detected).
- **Test File Pattern:** Files are named `*.test.ts` (suggests some TypeScript tests, possibly for frontend or API).
- **Backend Tests:** Located in `backend/tests/` (e.g., `test_agents.py`, `test_api.py`).
- **Typical Test Example:**
    ```python
    # backend/tests/test_agents.py
    import unittest
    from ..agents import Agent

    class TestAgent(unittest.TestCase):
        def test_agent_response(self):
            agent = Agent()
            self.assertIsNotNone(agent.respond("hello"))
    ```

## Commands

| Command           | Purpose                                                      |
|-------------------|--------------------------------------------------------------|
| /feature-backend  | Start a backend feature or hardening workflow                |
| /security-patch   | Apply security fixes, CVE patches, or update security docs   |
| /deploy-config    | Update deployment configuration (Render, Docker, etc.)        |
| /docs-update      | Add or update documentation and guides                       |
| /repo-cleanup     | Remove obsolete or legacy files/directories                   |
```
