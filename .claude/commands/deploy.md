# /project:deploy — Deploy to Render

Full deploy pipeline: qa → security scan → tests → push.

## Pre-deploy Checklist

Run `/project:qa` first. All 16 points must pass.

## Steps

```bash
# 1. QA check
/project:qa

# 2. Security scan
cd backend && backend/venv/bin/pip-audit
npm audit --prefix ../frontend

# 3. Full test suite
make test-backend

# 4. Build frontend
npm run build --prefix frontend

# 5. Commit and push
git add -A
git commit -m "chore: deploy v03"
git push origin v03
```

## Render Auto-Deploy

Render watches the `main` branch. To deploy:
1. Open a PR from `v03` → `main`
2. Wait for CI (pytest + frontend build) to pass
3. Merge — Render auto-deploys

## Post-Deploy Validation

```bash
curl https://80053-api.rudyprasetiya.com/api/health
# Expected: {"status": "ok", "db": "ok", "faiss": "ok"}

curl https://80053-api.rudyprasetiya.com/api/interactions/stats \
  -H "X-Api-Key: $API_KEY"
```
