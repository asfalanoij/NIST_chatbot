#!/usr/bin/env bash
# =============================================================================
# CI/CD Agent — Pipeline Readiness & Deployment Checks
# =============================================================================
# Usage: ./antigravity.sh cicd check
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-check}"

run_check() {
    header "CI/CD Agent — 10-Point Pipeline Readiness"

    # 1. Git repo initialized
    add_check
    if [ -d "${PROJECT_ROOT}/.git" ]; then
        pass_check "Git repository initialized"
    else
        fail_check "Not a git repository"
    fi

    # 2. .gitignore covers deployment artifacts
    add_check
    local missing=0
    for pattern in ".env" "venv/" "node_modules/" "__pycache__/" "*.db" ".logs/"; do
        if ! grep -q "$pattern" "${PROJECT_ROOT}/.gitignore" 2>/dev/null; then
            missing=$((missing + 1))
        fi
    done
    if [ "$missing" -eq 0 ]; then
        pass_check ".gitignore covers all deployment artifacts"
    else
        fail_check ".gitignore missing ${missing} critical patterns"
    fi

    # 3. Backend tests exist and are runnable
    add_check
    local test_count
    test_count=$(ls "${PROJECT_ROOT}"/backend/tests/test_*.py 2>/dev/null | wc -l | tr -d ' ')
    if [ "$test_count" -gt 0 ]; then
        pass_check "Backend test files found (${test_count} test modules)"
    else
        fail_check "No backend test files"
    fi

    # 4. Backend tests pass
    add_check
    if cd "${PROJECT_ROOT}/backend" && source venv/bin/activate 2>/dev/null && python -m pytest tests/ -q --tb=no 2>/dev/null; then
        local passed
        passed=$(cd "${PROJECT_ROOT}/backend" && source venv/bin/activate 2>/dev/null && python -m pytest tests/ -q --tb=no 2>&1 | tail -1 || echo "? passed")
        pass_check "Backend tests pass (${passed})"
    else
        fail_check "Backend tests fail"
    fi

    # 5. Frontend builds clean
    add_check
    if cd "${PROJECT_ROOT}/frontend" && npm run build --silent 2>/dev/null; then
        pass_check "Frontend builds clean"
    else
        fail_check "Frontend build fails"
    fi

    # 6. Requirements file is pinnable
    add_check
    if [ -f "${PROJECT_ROOT}/backend/requirements.txt" ]; then
        local unpinned
        unpinned=$(grep -c "^[a-zA-Z]" "${PROJECT_ROOT}/backend/requirements.txt" 2>/dev/null | tr -d '[:space:]' || echo "0")
        local pinned
        pinned=$(grep -c "==" "${PROJECT_ROOT}/backend/requirements.txt" 2>/dev/null | tr -d '[:space:]' || echo "0")
        if [ "$pinned" -gt 0 ]; then
            pass_check "Dependencies partially pinned (${pinned} pinned, ${unpinned} unpinned)"
        else
            warn "  No pinned versions — consider: pip freeze > requirements.txt"
            pass_check "requirements.txt exists (${unpinned} deps, unpinned)"
        fi
    else
        fail_check "requirements.txt missing"
    fi

    # 7. package.json has build script
    add_check
    if grep -q '"build"' "${PROJECT_ROOT}/frontend/package.json" 2>/dev/null; then
        pass_check "Frontend package.json has build script"
    else
        fail_check "Frontend missing build script"
    fi

    # 8. GitHub Actions workflow exists
    add_check
    if [ -f "${PROJECT_ROOT}/.github/workflows/ci.yml" ] || [ -f "${PROJECT_ROOT}/.github/workflows/ci.yaml" ]; then
        pass_check "GitHub Actions CI workflow found"
    else
        fail_check "No GitHub Actions workflow (.github/workflows/ci.yml)"
        dim "  Recommendation: Create CI pipeline for automated testing"
    fi

    # 9. Makefile has test target
    add_check
    if grep -q "^test" "${PROJECT_ROOT}/Makefile" 2>/dev/null; then
        pass_check "Makefile has test targets"
    else
        fail_check "Makefile missing test targets"
    fi

    # 10. No uncommitted sensitive files
    add_check
    if [ -d "${PROJECT_ROOT}/.git" ]; then
        local sensitive
        sensitive=$(git -C "${PROJECT_ROOT}" ls-files "*.env" ".env.*" "*.key" "*.pem" "credentials*" 2>/dev/null | grep -v ".env.example" || true)
        if [ -z "$sensitive" ]; then
            pass_check "No sensitive files tracked in git"
        else
            fail_check "Sensitive files tracked: $sensitive"
        fi
    else
        pass_check "Skipped (not a git repo)"
    fi

    print_score "CI/CD Score"
    log_to_file "cicd" "Check: ${SCORE}/${TOTAL}"
}

case "$SKILL" in
    check|"")
        run_check
        ;;
    summary)
        run_check 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh cicd check"
        exit 1
        ;;
esac
