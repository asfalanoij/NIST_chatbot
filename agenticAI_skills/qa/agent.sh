#!/usr/bin/env bash
# =============================================================================
# QA Inspector Agent — 16-Point Quality Inspection
# =============================================================================
# Usage: ./antigravity.sh qa inspect
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-inspect}"

run_inspect() {
    header "QA Inspector — 16-Point Inspection"

    # 1. Backend directory exists
    add_check
    if [ -d "${PROJECT_ROOT}/backend" ]; then
        pass_check "Backend directory exists"
    else
        fail_check "Backend directory missing"
    fi

    # 2. Frontend directory exists
    add_check
    if [ -d "${PROJECT_ROOT}/frontend" ]; then
        pass_check "Frontend directory exists"
    else
        fail_check "Frontend directory missing"
    fi

    # 3. requirements.txt exists
    add_check
    if [ -f "${PROJECT_ROOT}/backend/requirements.txt" ]; then
        pass_check "backend/requirements.txt exists"
    else
        fail_check "backend/requirements.txt missing"
    fi

    # 4. package.json exists
    add_check
    if [ -f "${PROJECT_ROOT}/frontend/package.json" ]; then
        pass_check "frontend/package.json exists"
    else
        fail_check "frontend/package.json missing"
    fi

    # 5. .env.example exists
    add_check
    if [ -f "${PROJECT_ROOT}/.env.example" ]; then
        pass_check ".env.example exists"
    else
        fail_check ".env.example missing"
    fi

    # 6. .gitignore exists and covers essentials
    add_check
    if [ -f "${PROJECT_ROOT}/.gitignore" ] && grep -q "\.env" "${PROJECT_ROOT}/.gitignore"; then
        pass_check ".gitignore exists and covers .env"
    else
        fail_check ".gitignore missing or incomplete"
    fi

    # 7. README.md exists and is non-trivial
    add_check
    if [ -f "${PROJECT_ROOT}/README.md" ] && [ "$(wc -l < "${PROJECT_ROOT}/README.md")" -gt 20 ]; then
        pass_check "README.md exists ($(wc -l < "${PROJECT_ROOT}/README.md") lines)"
    else
        fail_check "README.md missing or too short"
    fi

    # 8. Backend tests exist
    add_check
    if [ -d "${PROJECT_ROOT}/backend/tests" ] && ls "${PROJECT_ROOT}"/backend/tests/test_*.py &>/dev/null; then
        pass_check "Backend tests exist"
    else
        fail_check "Backend tests missing (backend/tests/test_*.py)"
    fi

    # 9. Backend tests pass
    add_check
    if [ -d "${PROJECT_ROOT}/backend/tests" ]; then
        if cd "${PROJECT_ROOT}/backend" && source venv/bin/activate 2>/dev/null && python -m pytest tests/ -q --tb=no 2>/dev/null; then
            pass_check "Backend tests pass"
        else
            fail_check "Backend tests fail or cannot run"
        fi
    else
        fail_check "No tests to run"
    fi

    # 10. Frontend builds clean
    add_check
    if cd "${PROJECT_ROOT}/frontend" && npm run build --silent 2>/dev/null; then
        pass_check "Frontend builds clean"
    else
        fail_check "Frontend build fails"
    fi

    # 11. No secrets in source code
    add_check
    local secret_hits
    secret_hits=$(grep -rn "sk-\|AKIA\|ghp_\|password\s*=" "${PROJECT_ROOT}/backend/" "${PROJECT_ROOT}/frontend/src/" --include="*.py" --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v "node_modules" | grep -v "venv" | grep -v ".env.example" || true)
    if [ -z "$secret_hits" ]; then
        pass_check "No secrets detected in source"
    else
        fail_check "Potential secrets in source code"
        echo "$secret_hits" | head -5
    fi

    # 12. CORS not wildcard in production
    add_check
    if grep -q 'CORS(app)' "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
        if grep -q 'CORS_ORIGINS\|origins=' "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
            pass_check "CORS configured with specific origins"
        else
            fail_check "CORS uses wildcard (CORS(app) without origins)"
        fi
    else
        pass_check "CORS configuration present"
    fi

    # 13. API health endpoint works (if server is running)
    add_check
    if curl -s http://localhost:5050/api/health 2>/dev/null | grep -q "healthy"; then
        pass_check "/api/health returns healthy"
    else
        fail_check "/api/health not responding (is backend running?)"
    fi

    # 14. Vector index exists
    add_check
    if [ -f "${PROJECT_ROOT}/backend/index_kms/index.faiss" ]; then
        pass_check "FAISS vector index exists"
    else
        fail_check "FAISS vector index missing (run make ingest)"
    fi

    # 15. All 13 build agents operational
    add_check
    local agent_count=0
    for agent_dir in qa devsecops nist-expert data-scientist pm e2e-test context-optimizer visitor-tracker api-auth api-loadtest rag-evaluator chat-export cicd; do
        if [ -f "${SKILLS_DIR}/${agent_dir}/agent.sh" ]; then
            agent_count=$((agent_count + 1))
        fi
    done
    if [ "$agent_count" -eq 13 ]; then
        pass_check "All 13 build agents present"
    else
        fail_check "Only ${agent_count}/13 build agents found"
    fi

    # 16. Visitor tracking endpoint
    add_check
    if curl -s http://localhost:5050/api/visitors/count 2>/dev/null | grep -q "unique_visitors"; then
        pass_check "/api/visitors/count responds"
    else
        fail_check "/api/visitors/count not responding"
    fi

    print_score "QA Score"
    log_to_file "qa" "Inspection: ${SCORE}/${TOTAL}"
}

case "$SKILL" in
    inspect|"")
        run_inspect
        ;;
    summary)
        run_inspect 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh qa inspect"
        exit 1
        ;;
esac
