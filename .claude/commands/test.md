# /project:test — Run Backend Tests

Run the full pytest suite against the backend.

```bash
cd /Users/asfalanoi/app_oct2025/NIST_chatbot_v02/backend
./venv/bin/python -m pytest tests/ -v --tb=short
```

## Expected Output

- 38+ tests passing
- 0 failures, 0 errors
- Coverage report if `pytest-cov` is installed: `--cov=. --cov-report=term-missing`

## Makefile Shortcut

```bash
make test-backend
```
