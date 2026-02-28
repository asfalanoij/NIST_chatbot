# Render Deployment Guide — NIST Chatbot v2.0.0

## Prerequisites
- GitHub repo merged to `main`: https://github.com/asfalanoij/NIST_chatbot
- FAISS index uploaded to GitHub Release v2.0.0
- Gemini API key ready

## Step 1: Connect Render to GitHub
1. Go to https://render.com → Sign up / Log in
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select repo: **asfalanoij/NIST_chatbot**
5. Render reads `render.yaml` automatically → shows 3 services:
   - `nist-chatbot-api` (Web Service, Docker)
   - `nist-chatbot-frontend` (Static Site)
   - `nist-chatbot-db` (PostgreSQL, free tier)

## Step 2: Set Environment Variables
When Render prompts for env vars:
- **GEMINI_API_KEY**: paste your Gemini API key
- Others are auto-configured from render.yaml

## Step 3: Deploy
1. Click **"Apply"** → Render builds and deploys all 3 services
2. Backend builds Docker image (downloads FAISS index from GitHub Release)
3. Frontend runs `npm install && npm run build`, serves from `dist/`
4. PostgreSQL provisions automatically

## Step 4: Custom Domain (80053.rudyprasetiya.com)

### Backend API domain:
1. In Render dashboard → `nist-chatbot-api` → Settings → Custom Domains
2. Add: `80053-api.rudyprasetiya.com`
3. Render gives you a CNAME target (e.g., `nist-chatbot-api.onrender.com`)

### Frontend domain:
1. In Render → `nist-chatbot-frontend` → Settings → Custom Domains
2. Add: `80053.rudyprasetiya.com`
3. Render gives you a CNAME target

### DNS (Cloudflare — nameservers confirmed at paige/viddy.ns.cloudflare.com):
Add two CNAME records in Cloudflare dashboard → DNS → Records:
```
80053        CNAME  nist-chatbot-frontend.onrender.com  [DNS only — grey cloud]
80053-api    CNAME  nist-chatbot-api.onrender.com       [DNS only — grey cloud]
```
**IMPORTANT**: Set proxy to **DNS only (grey cloud)**. Orange cloud (proxied) causes SSL 525 error.
Do NOT use A records — use CNAME only.

TLS is automatic — Render provisions Let's Encrypt certificates.

## Step 5: Verify
- https://80053-api.rudyprasetiya.com/api/health → should return `{"status": "healthy"}`
- https://80053.rudyprasetiya.com → frontend loads
- Test a chat query

## Step 6: Re-enable ruleset
Already done ✓ (prudent ruleset re-enabled)

## Notes
- `DISABLE_INGEST=true` is set in render.yaml — no one can re-ingest in prod
- Rate limits: 10/min chat, 5/min ingest
- To update FAISS index: re-ingest locally, upload new files to a GitHub Release, update Dockerfile URL, redeploy
- Render free tier PostgreSQL: 1GB, auto-sleeps after 90 days of inactivity
- Render starter plan: ~$7/mo for the web service
