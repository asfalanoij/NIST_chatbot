# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.x     | ✓ Active  |
| 1.x     | ✗ End of life |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities privately via GitHub's Security Advisory:
👉 https://github.com/asfalanoij/NIST_chatbot/security/advisories/new

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

You will receive a response within **72 hours**. If the vulnerability is confirmed, a patch will be released and you will be credited in the release notes (unless you prefer to remain anonymous).

## Scope

| In scope | Out of scope |
|----------|-------------|
| Backend API (`/api/*`) | Third-party LLM providers (Gemini, Ollama) |
| Authentication (`X-API-Key`) | Render hosting infrastructure |
| RAG pipeline / FAISS index | Social engineering |
| Frontend (XSS, CSRF) | DoS / rate-limit bypass attempts |
| Dependency vulnerabilities | |

## Security Measures

- **API authentication** — `X-API-Key` header required on write endpoints
- **Rate limiting** — 10 req/min chat, 5 req/min ingest (flask-limiter)
- **CORS** — locked to configured origins only
- **No secrets in code** — all configuration via environment variables
- **Ingestion disabled in production** — `DISABLE_INGEST=true`
- **Dependency monitoring** — GitHub Dependabot with auto-alerts
- **HTTPS only** — TLS enforced via Render + Let's Encrypt

## Known Limitations

- The free Render tier sleeps after inactivity — this is a hosting constraint, not a security issue
- The FAISS index is read-only in production; ingestion requires a valid API key
