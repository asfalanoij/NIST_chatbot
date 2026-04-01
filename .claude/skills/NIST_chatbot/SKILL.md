```markdown
# NIST_chatbot Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill describes the core development patterns, coding conventions, and workflows used in the `NIST_chatbot` Python codebase. It covers backend feature development, production deployment, documentation practices, dependency management, and repository cleanup. By following these guidelines, contributors can maintain code consistency, streamline collaboration, and ensure high code quality.

## Coding Conventions

**File Naming**
- Use `camelCase` for file names.
  - Example: `interactionLog.py`, `ragEngine.py`

**Import Style**
- Use relative imports within modules.
  - Example:
    ```python
    from .schemas import UserInput
    from .cache import CacheManager
    ```

**Export Style**
- Use default exports (i.e., define classes/functions at module level without explicit `__all__` unless needed).
  - Example:
    ```python
    class RagEngine:
        ...
    ```

**Commit Message Patterns**
- Prefix commits with `fix`, `feat`, `chore`, or `docs`.
  - Example: `feat: add RAG engine for document retrieval`
- Keep commit messages concise (average 53 characters).

## Workflows

### Backend Feature Development with Tests
**Trigger:** When adding or updating backend features, endpoints, or modules.  
**Command:** `/new-backend-feature`

1. Create or update backend implementation files (e.g., `agents.py`, `app.py`, `rag_engine.py`, `schemas.py`, `cache.py`, `interaction_log.py`).
2. Add or update corresponding test files in `backend/tests/` (e.g., `test_agents.py`, `test_api.py`, `test_cache.py`, `test_interaction_log.py`, `test_schemas.py`).
3. Update `Makefile` or requirements files if new dependencies are introduced.
4. Update `.gitignore` if new artifacts or build outputs are generated.

**Example:**
```python
# backend/agents.py
class ChatAgent:
    def respond(self, message: str) -> str:
        # Implementation here
        pass

# backend/tests/test_agents.py
def test_chat_agent_response():
    agent = ChatAgent()
    assert agent.respond("Hello") == "Expected response"
```

---

### Production Deployment Configuration
**Trigger:** When deploying or updating the app in production or staging environments.  
**Command:** `/deploy-config`

1. Edit `render.yaml` to update deployment settings (e.g., domains, API URLs).
2. Edit or add `backend/Dockerfile` and `backend/Procfile` for containerization and WSGI setup.
3. Update `.github/workflows/ci.yml` for CI/CD pipeline changes.
4. Update frontend config files (e.g., `frontend/src/config.ts`) for API base URLs.
5. Commit and merge changes to the `main` or `production` branch.

**Example:**
```yaml
# render.yaml
services:
  - type: web
    name: nist-chatbot-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

---

### Documentation and Policy Update
**Trigger:** When documenting new features, updating security policies, or providing deployment instructions.  
**Command:** `/doc-update`

1. Edit or add markdown files for documentation (e.g., `README.md`, `SECURITY.md`, `CLAUDE.md`, `workflows/*.md`).
2. Update or add `.claude/` rules, commands, agents, or skills documentation.
3. Commit documentation changes, often alongside or after feature development.

**Example:**
```markdown
# README.md
## New Feature: RAG Engine
The RAG engine enables document retrieval for chat responses.
```

---

### Dependency and Security Patch
**Trigger:** When updating dependencies for security or compatibility reasons.  
**Command:** `/patch-deps`

1. Update `backend/requirements.txt` and/or `backend/requirements-dev.txt`.
2. Update frontend dependencies as needed (e.g., via `npm update`).
3. Update `Makefile` or `.gitignore` if necessary.
4. Document the change in `README.md` or commit message.

**Example:**
```txt
# backend/requirements.txt
fastapi==0.95.2
gunicorn==20.1.0
```

---

### Repo Cleanup and Legacy Removal
**Trigger:** When removing obsolete, legacy, or experimental files and directories.  
**Command:** `/repo-cleanup`

1. Delete legacy folders (e.g., `legacy/`, `rag-mvp/`, `inspo_CSS_chatbot_app/`).
2. Delete unused screenshots, notes, or duplicate files.
3. Update `.gitignore` if necessary.
4. Document the cleanup in the commit message.

**Example:**
```bash
git rm -r legacy/ rag-mvp/ inspo_CSS_chatbot_app/
```

## Testing Patterns

- Test files are located in `backend/tests/` and named as `test_*.py`.
- Each test module targets a specific backend module (e.g., `test_agents.py` for `agents.py`).
- Testing framework is not explicitly stated; likely uses `pytest` or standard Python `unittest`.
- Typical test structure:
    ```python
    # backend/tests/test_cache.py
    def test_cache_set_and_get():
        cache = CacheManager()
        cache.set("key", "value")
        assert cache.get("key") == "value"
    ```

## Commands

| Command              | Purpose                                               |
|----------------------|-------------------------------------------------------|
| /new-backend-feature | Start backend feature/module development with tests   |
| /deploy-config       | Update deployment, Docker, or CI/CD configuration     |
| /doc-update          | Add or update documentation and policy files          |
| /patch-deps          | Patch or upgrade dependencies for security/compatibility |
| /repo-cleanup        | Remove obsolete or legacy files from the repository   |
```