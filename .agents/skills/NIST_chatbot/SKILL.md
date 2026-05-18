```markdown
# NIST_chatbot Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill teaches you how to contribute to the NIST_chatbot Python codebase, following its unique conventions and workflows. You'll learn the project's coding style, how to develop and harden backend features, manage dependencies, update deployment configurations, and maintain documentation. The repository is Python-based, with no major framework, and is structured for clarity, maintainability, and secure deployment.

## Coding Conventions

- **File Naming:**  
  Use `camelCase` for file names.  
  _Example:_  
  ```
  visitorTracker.py
  interactionLog.py
  ```

- **Import Style:**  
  Use **relative imports** within modules.  
  _Example:_  
  ```python
  from .agents import AgentManager
  from .cache import Cache
  ```

- **Export Style:**  
  Use **default exports** (Python modules/classes/functions as usual).  
  _Example:_  
  ```python
  class VisitorTracker:
      ...
  ```

- **Commit Messages:**  
  - Mixed types: `fix`, `feat`, `chore`, `docs`, `ci`, `security`
  - Prefix each commit with the type, e.g., `fix:`, `feat:`
  - Average message length: ~55 characters

## Workflows

### Backend Feature Development and Hardening
**Trigger:** When developing a new backend feature or applying a security/hardening fix  
**Command:** `/feature-backend`

1. Edit or add backend Python modules (e.g., `backend/app.py`, `backend/agents.py`, `backend/visitorTracker.py`, etc.)
2. Update or add tests in `backend/tests/` (e.g., `test_api.py`, `test_agents.py`)
3. Update `backend/requirements.txt` and/or `backend/requirements-dev.txt` if dependencies change
4. Optionally update `Makefile` or `.gitignore`
5. Commit all changes together

_Example:_
```python
# backend/agents.py
class NewAgent:
    ...
```
```python
# backend/tests/test_agents.py
def test_new_agent():
    ...
```

### CI/CD Pipeline Update or Deployment Workflow
**Trigger:** When setting up or modifying deployment or CI/CD (e.g., new VPS, Render, or security scanning)  
**Command:** `/deploy-config`

1. Edit or add `.github/workflows/*.yml` for CI/CD
2. Edit or add deployment files (`docker-compose.prod.yml`, `render.yaml`, `nginx/nist-chatbot.conf`, `backend/Dockerfile`, `backend/Procfile`, etc.)
3. Update `.gitignore` if new secrets/configs are introduced
4. Commit all changes together

_Example:_
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      ...
```

### Documentation and Policy Update
**Trigger:** When documenting new features, deployment steps, or security policies  
**Command:** `/docs-update`

1. Edit or add documentation files (`README.md`, `SECURITY.md`, deployment guides, etc.)
2. Commit documentation changes (sometimes with related config or code updates)

_Example:_
```markdown
# SECURITY.md
## Reporting a Vulnerability
...
```

### Dependency Upgrade and Security Patch
**Trigger:** When upgrading dependencies for security or compatibility  
**Command:** `/upgrade-deps`

1. Update `backend/requirements.txt` and/or `backend/requirements-dev.txt`
2. Update code as needed for compatibility (e.g., `backend/app.py`, `backend/agents.py`)
3. Update tests if necessary
4. Commit all changes together

_Example:_
```
# backend/requirements.txt
fastapi==0.95.0
```

### Deployment Config Tweak (Render YAML)
**Trigger:** When changing Render deployment settings (tier, domain, API key, etc.)  
**Command:** `/render-config`

1. Edit `render.yaml` with the required deployment config change
2. Commit the change (sometimes as part of a merge from dev branch)

_Example:_
```yaml
# render.yaml
services:
  - type: web
    name: nist-chatbot
    env: python
    ...
```

## Testing Patterns

- **Framework:** Unknown (not explicitly detected)
- **Test File Pattern:** `*.test.ts` (suggests some TypeScript tests, but main backend tests are in Python under `backend/tests/`)
- **Python Test Example:**
  ```python
  # backend/tests/test_api.py
  def test_api_returns_200():
      response = client.get("/api")
      assert response.status_code == 200
  ```

## Commands

| Command           | Purpose                                                      |
|-------------------|--------------------------------------------------------------|
| /feature-backend  | Start backend feature development or hardening workflow       |
| /deploy-config    | Update CI/CD pipeline or deployment configuration            |
| /docs-update      | Update documentation or policy files                         |
| /upgrade-deps     | Upgrade dependencies and patch security issues               |
| /render-config    | Apply tweaks to Render deployment configuration              |
```
