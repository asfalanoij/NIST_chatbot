```markdown
# NIST_chatbot Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill teaches you how to contribute to the NIST_chatbot Python codebase, following its unique conventions and established workflows. You'll learn file organization, code style, commit practices, and how to perform common tasks such as adding backend features, patching security issues, updating deployment configs, improving documentation, and cleaning up legacy code. The repository is backend-focused, with no major framework, and emphasizes robust testing and security practices.

---

## Coding Conventions

- **File Naming:**  
  Use `camelCase` for Python files (e.g., `ragEngine.py`, `visitorTracker.py`).

- **Import Style:**  
  Use **relative imports** within the backend modules.
  ```python
  # Example from backend/agents.py
  from .ragEngine import RagEngine
  from .visitorTracker import VisitorTracker
  ```

- **Export Style:**  
  Use **default exports** (i.e., define main classes/functions at the module level).
  ```python
  # backend/agents.py
  class Agent:
      ...
  ```

- **Commit Messages:**  
  - Use prefixes: `fix:`, `feat:`, `chore:`, `docs:`, `security:`
  - Keep messages concise (~54 characters on average)
  - Example:  
    ```
    feat: add visitor tracking to backend and update tests
    ```

---

## Workflows

### Backend Feature or Refactor with Tests
**Trigger:** When adding, changing, or refactoring backend logic (agents, RAG, visitor tracking, etc.)  
**Command:** `/feature-backend`

1. Edit or add backend Python modules (e.g., `agents.py`, `ragEngine.py`, `visitorTracker.py`, `crossmap.py`).
2. Update or add corresponding test files in `backend/tests/`.
3. Update `requirements.txt` or `requirements-dev.txt` if dependencies change.

**Example:**
```python
# backend/agents.py
class Agent:
    def __init__(self, name):
        self.name = name

# backend/tests/test_agents.py
def test_agent_init():
    agent = Agent("Claude")
    assert agent.name == "Claude"
```

---

### Security Hardening and CVE Patch
**Trigger:** When addressing a security vulnerability or hardening the backend  
**Command:** `/security-patch`

1. Update `backend/requirements.txt` and/or `requirements-dev.txt` to patch dependencies.
2. Edit `backend/app.py` and related modules to improve security (e.g., headers, error handling).
3. Add or update security tests in `backend/tests/test_api.py` or similar.
4. Update `.github/workflows/ci.yml` to enforce security checks.
5. Update or add documentation (`README.md`, `SECURITY.md`).

**Example:**
```python
# backend/app.py
from flask import Flask
app = Flask(__name__)

@app.after_request
def set_secure_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
```

---

### Deployment Config Update
**Trigger:** When changing deployment settings, environment, or infrastructure  
**Command:** `/deploy-config`

1. Edit `render.yaml` for Render deployment changes.
2. Edit `backend/Dockerfile` and/or `backend/Procfile` for backend service changes.
3. Update `.github/workflows/ci.yml` for CI/CD pipeline changes.
4. Update `.env.example` or `Makefile` if needed.

**Example:**
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

---

### Documentation and Policy Update
**Trigger:** When clarifying, updating, or adding documentation or policies  
**Command:** `/docs-update`

1. Edit or add `README.md`, `SECURITY.md`, or other docs.
2. Add or update deployment guides in `agenticAI_skills/workflows/`.
3. Update `.claude/` or similar meta/config files if relevant.

**Example:**
```markdown
# SECURITY.md
## Reporting a Vulnerability
Please open an issue or contact the maintainers.
```

---

### Repo Cleanup or Legacy Removal
**Trigger:** When removing old code, design artifacts, or duplicated files  
**Command:** `/cleanup`

1. Delete legacy directories (e.g., `legacy/`, `rag-mvp/`, `inspo_CSS_chatbot_app/`).
2. Remove root-level screenshots or notes.
3. Remove duplicate or unused files (e.g., `requirements.txt`, test scripts).

**Example:**
```bash
git rm -r legacy/ rag-mvp/ inspo_CSS_chatbot_app/
git rm *.png *.txt test_gemini_index.py
```

---

## Testing Patterns

- **Test Framework:** Unknown (likely `pytest` based on file naming)
- **Test File Pattern:** Place tests in `backend/tests/` with filenames like `test_*.py`.
- **Test Example:**
  ```python
  # backend/tests/test_ragEngine.py
  def test_rag_engine_response():
      engine = RagEngine()
      assert engine.respond("hello") == "Hi, how can I help you?"
  ```
- **Best Practice:** Update or add tests whenever you change backend logic.

---

## Commands

| Command           | Purpose                                              |
|-------------------|------------------------------------------------------|
| /feature-backend  | Add or refactor backend features with tests          |
| /security-patch   | Apply security fixes and update security docs/tests  |
| /deploy-config    | Update deployment configuration or infrastructure    |
| /docs-update      | Add or update documentation and policy files         |
| /cleanup          | Remove legacy, obsolete, or duplicate files          |
```
