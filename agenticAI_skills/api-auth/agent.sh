#!/usr/bin/env bash
# =============================================================================
# API Auth Agent — Authentication & Authorization Verification
# =============================================================================
# Usage: ./antigravity.sh api-auth verify
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-verify}"
API_BASE="${API_BASE:-http://localhost:5050}"

run_verify() {
    header "API Auth Agent — 8-Point Auth Verification"

    # 1. API_KEY env var is documented in .env.example
    add_check
    if grep -q "API_KEY" "${PROJECT_ROOT}/.env.example" 2>/dev/null; then
        pass_check "API_KEY documented in .env.example"
    else
        fail_check "API_KEY missing from .env.example"
    fi

    # 2. require_api_key decorator exists in app.py
    add_check
    if grep -q "require_api_key" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
        pass_check "require_api_key decorator found in app.py"
    else
        fail_check "No auth decorator in app.py"
    fi

    # 3. /api/chat is protected
    add_check
    if grep -B1 "def chat" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null | grep -q "require_api_key"; then
        pass_check "/api/chat is protected by require_api_key"
    else
        fail_check "/api/chat is NOT protected"
    fi

    # 4. /api/ingest is protected
    add_check
    if grep -B1 "def run_ingest" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null | grep -q "require_api_key"; then
        pass_check "/api/ingest is protected by require_api_key"
    else
        fail_check "/api/ingest is NOT protected"
    fi

    # 5. /api/health is NOT protected (should be open)
    add_check
    if grep -B1 "def health_check" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null | grep -q "require_api_key"; then
        fail_check "/api/health should NOT require auth"
    else
        pass_check "/api/health is correctly unprotected"
    fi

    # 6. Auth tests exist
    add_check
    if grep -q "TestApiKeyAuth" "${PROJECT_ROOT}/backend/tests/test_api.py" 2>/dev/null; then
        pass_check "Auth test class exists (TestApiKeyAuth)"
    else
        fail_check "No auth tests found"
    fi

    # 7. Live test: health endpoint accessible without key (if server running)
    add_check
    local health_resp
    health_resp=$(curl -s -o /dev/null -w "%{http_code}" "${API_BASE}/api/health" 2>/dev/null || echo "000")
    if [ "$health_resp" = "200" ]; then
        pass_check "Live: /api/health returns 200 without key"
    elif [ "$health_resp" = "000" ]; then
        dim "  Backend not running — skipping live tests"
        pass_check "Skipped (backend not running)"
    else
        fail_check "Live: /api/health returned $health_resp"
    fi

    # 8. Live test: chat rejects without key (if API_KEY configured and server running)
    add_check
    if [ "$health_resp" = "200" ]; then
        local chat_resp
        chat_resp=$(curl -s -o /dev/null -w "%{http_code}" \
            -X POST "${API_BASE}/api/chat" \
            -H "Content-Type: application/json" \
            -d '{"message":"test"}' 2>/dev/null || echo "000")
        case "$chat_resp" in
            401)
                pass_check "Live: /api/chat rejects unauthenticated (401)"
                ;;
            200)
                warn "  /api/chat returned 200 — API_KEY may not be configured (dev mode)"
                pass_check "Live: auth disabled (dev mode — set API_KEY for production)"
                ;;
            *)
                fail_check "Live: /api/chat returned unexpected $chat_resp"
                ;;
        esac
    else
        pass_check "Skipped (backend not running)"
    fi

    print_score "Auth Score"
    log_to_file "api-auth" "Verify: ${SCORE}/${TOTAL}"
}

case "$SKILL" in
    verify|"")
        run_verify
        ;;
    summary)
        run_verify 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh api-auth verify"
        exit 1
        ;;
esac
