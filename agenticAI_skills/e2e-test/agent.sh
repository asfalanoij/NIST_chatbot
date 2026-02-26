#!/usr/bin/env bash
# =============================================================================
# E2E Test Agent — Test Orchestration
# =============================================================================
# Usage: ./antigravity.sh e2e-test run
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-run}"

run_backend_tests() {
    header "E2E Test Agent — Backend Tests"

    add_check
    if [ -d "${PROJECT_ROOT}/backend/tests" ]; then
        info "Running pytest..."
        if cd "${PROJECT_ROOT}/backend" && source venv/bin/activate 2>/dev/null && python -m pytest tests/ -v 2>&1; then
            pass_check "Backend tests passed"
        else
            fail_check "Backend tests failed"
        fi
    else
        fail_check "No backend tests directory"
    fi
}

run_frontend_build() {
    header "E2E Test Agent — Frontend Build"

    add_check
    info "Running npm run build..."
    if cd "${PROJECT_ROOT}/frontend" && npm run build 2>&1; then
        pass_check "Frontend build succeeded"
    else
        fail_check "Frontend build failed"
    fi
}

run_health_check() {
    header "E2E Test Agent — API Health"

    add_check
    if curl -s --max-time 5 http://localhost:5050/api/health 2>/dev/null | grep -q "healthy"; then
        pass_check "Backend API is healthy"
    else
        fail_check "Backend API not responding"
    fi

    add_check
    if curl -s --max-time 5 http://localhost:5173 2>/dev/null | grep -q "html"; then
        pass_check "Frontend dev server is running"
    else
        fail_check "Frontend dev server not responding (is it running?)"
    fi
}

run_all() {
    run_backend_tests
    run_frontend_build
    run_health_check
    print_score "E2E Score"
    log_to_file "e2e-test" "Run: ${SCORE}/${TOTAL}"
}

case "$SKILL" in
    run|"")
        run_all
        ;;
    backend)
        run_backend_tests
        print_score "Backend Test Score"
        ;;
    frontend)
        run_frontend_build
        print_score "Frontend Build Score"
        ;;
    health)
        run_health_check
        print_score "Health Check Score"
        ;;
    summary)
        run_all 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh e2e-test [run|backend|frontend|health]"
        exit 1
        ;;
esac
