```markdown
# NIST_chatbot Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill teaches the core development patterns and workflows used in the `NIST_chatbot` Python codebase. The repository is a backend-focused chatbot project, with no major framework detected, and emphasizes secure, maintainable, and well-documented code. You'll learn conventions for file organization, coding style, commit hygiene, and how to contribute using established workflows for features, security, deployment, documentation, and cleanup.

---

## Coding Conventions

**File Naming:**  
- Use `camelCase` for Python files and modules.
  - Example: `visitorTracker.py`, `ragEngine.py`

**Import Style:**  
- Use relative imports within modules.
  - Example:
    ```python
    from .utils import sanitize_input
    from . import visitorTracker
    ```

**Export Style:**  
- Use default exports (i.e., define main classes or functions at the module level).
  - Example:
    ```python
    # In ragEngine.py
    class RagEngine:
        ...
    ```

**Commit Messages:**  
- Prefix with type: `fix`, `feat`, `chore`, `docs`, `ci`, `security`
- Keep messages concise (average ~54 characters).
  - Example:  
    ```
    feat: add visitor tracking to backend
    fix: sanitize user input for CVE-2024-xxxx
    ```

---

## Workflows

### Backend Feature Development and Hardening
**Trigger:** When you want to add or refactor backend features, or improve security.  
**Command:** `/backend-feature`

1. Edit or add backend Python files (e.g., `backend/agents.py`, `backend/app.py`).
2. Update `backend/requirements.txt` and/or `backend/requirements-dev.txt` if dependencies change.
3. Add or update test files in `backend/tests/`.
4. Update `.gitignore` or `Makefile` if needed.

**Example:**
```python
# backend/visitorTracker.py
class VisitorTracker:
    def track(self, user_id):
        # logic here
        pass
```
```bash
pip install new-dependency
echo "new-dependency" >> backend/requirements.txt
```

---

### Security Patch and CVE Mitigation
**Trigger:** When a new CVE or security issue is discovered in dependencies or code.  
**Command:** `/security-patch`

1. Update affected dependencies in `requirements.txt` (and `requirements-dev.txt` if needed).
2. Patch backend code to mitigate vulnerabilities (e.g., sanitize input).
3. Add or update security-related tests in `backend/tests/`.
4. Update CI workflow to add security checks (e.g., `bandit`, `pip-audit`).

**Example:**
```python
# backend/app.py
from .utils import sanitize_input

def handle_input(user_input):
    safe_input = sanitize_input(user_input)
    ...
```
```yaml
# .github/workflows/ci.yml
- name: Run Bandit Security Scan
  run: bandit -r backend/
```

---

### Deployment Configuration Update
**Trigger:** When deployment targets, domains, or infrastructure change.  
**Command:** `/update-deployment`

1. Edit deployment config files (`render.yaml`, `docker-compose.prod.yml`, `nginx/*.conf`).
2. Update environment files or `.gitignore` as needed.
3. Change CI/CD workflow files to match new deployment process.
4. Document deployment steps if needed.

**Example:**
```yaml
# docker-compose.prod.yml
services:
  chatbot:
    build: .
    environment:
      - ENV=production
```

---

### Documentation and Policy Update
**Trigger:** When documentation or policy needs to be added or clarified.  
**Command:** `/update-docs`

1. Edit or add markdown files (`README.md`, `SECURITY.md`, deployment guides, etc.).
2. Update documentation in `agenticAI_skills/workflows/` or root.
3. Sometimes update config files to match documented steps.

**Example:**
```markdown
# SECURITY.md
## Reporting a Vulnerability
Please email security@domain.com.
```

---

### Cleanup and Legacy Artifact Removal
**Trigger:** When legacy code or unused files should be deleted.  
**Command:** `/cleanup`

1. Delete legacy folders (e.g., `legacy/`, `rag-mvp/`, `inspo_CSS_chatbot_app/`).
2. Remove root-level screenshots or notes (`*.png`, `*.txt`).
3. Clean up duplicate or obsolete files.

**Example:**
```bash
rm -rf legacy/ rag-mvp/ inspo_CSS_chatbot_app/
rm *.png *.txt
```

---

## Testing Patterns

- **Framework:** Unknown (no explicit framework detected).
- **Test File Pattern:** Python test files are in `backend/tests/` and named with `.py` extension.
- **Best Practice:** Add or update tests when making changes to backend logic or security.
- **Example:**
    ```python
    # backend/tests/test_visitorTracker.py
    from backend.visitorTracker import VisitorTracker

    def test_track():
        tracker = VisitorTracker()
        assert tracker.track('user123') is not None
    ```

---

## Commands

| Command            | Purpose                                                    |
|--------------------|------------------------------------------------------------|
| /backend-feature   | Start a backend feature, refactor, or security improvement |
| /security-patch    | Apply security patch or CVE mitigation                     |
| /update-deployment | Update deployment configuration or infrastructure          |
| /update-docs       | Add or update documentation or policy                      |
| /cleanup           | Remove legacy code or obsolete files                       |
```
