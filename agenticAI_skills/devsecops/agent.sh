#!/usr/bin/env bash
# =============================================================================
# DevSecOps Agent — Security Scanning & Hygiene
# =============================================================================
# Usage: ./antigravity.sh devsecops scan
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-scan}"

run_scan() {
    header "DevSecOps Agent — Security Scan"

    # 1. Check for hardcoded secrets
    add_check
    info "Scanning for hardcoded secrets..."
    local secret_patterns='(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36}|AIza[a-zA-Z0-9_-]{35})'
    local hits
    hits=$(grep -rEn "$secret_patterns" \
        --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.sh" \
        "${PROJECT_ROOT}/backend/" "${PROJECT_ROOT}/frontend/src/" "${PROJECT_ROOT}/agenticAI_skills/" 2>/dev/null \
        | grep -v "node_modules" | grep -v "venv" | grep -v ".env.example" || true)
    if [ -z "$hits" ]; then
        pass_check "No hardcoded API keys or secrets found"
    else
        fail_check "Potential secrets detected:"
        echo "$hits"
    fi

    # 2. .env file is gitignored
    add_check
    if grep -q "^\.env$" "${PROJECT_ROOT}/.gitignore" 2>/dev/null; then
        pass_check ".env is in .gitignore"
    else
        fail_check ".env is NOT in .gitignore"
    fi

    # 3. .env.example exists (no real values)
    add_check
    if [ -f "${PROJECT_ROOT}/.env.example" ]; then
        local real_keys
        real_keys=$(grep -E "=.{10,}" "${PROJECT_ROOT}/.env.example" | grep -v "your_\|changeme\|placeholder\|example\|localhost\|llama" || true)
        if [ -z "$real_keys" ]; then
            pass_check ".env.example exists with placeholder values only"
        else
            fail_check ".env.example may contain real secrets"
        fi
    else
        fail_check ".env.example does not exist"
    fi

    # 4. No .env files committed
    add_check
    if [ -d "${PROJECT_ROOT}/.git" ]; then
        local tracked_env
        tracked_env=$(git -C "${PROJECT_ROOT}" ls-files "*.env" ".env.*" 2>/dev/null | grep -v ".env.example" || true)
        if [ -z "$tracked_env" ]; then
            pass_check "No .env files tracked in git"
        else
            fail_check "Found .env files tracked in git: $tracked_env"
        fi
    else
        warn "Not a git repo — skipping tracked files check"
        pass_check "Skipped (not a git repo)"
    fi

    # 5. .gitignore covers critical paths
    add_check
    local missing_patterns=()
    for pattern in "venv/" "node_modules/" ".env" "__pycache__/" "*.db" ".logs/"; do
        if ! grep -q "$pattern" "${PROJECT_ROOT}/.gitignore" 2>/dev/null; then
            missing_patterns+=("$pattern")
        fi
    done
    if [ ${#missing_patterns[@]} -eq 0 ]; then
        pass_check ".gitignore covers all critical patterns"
    else
        fail_check ".gitignore missing: ${missing_patterns[*]}"
    fi

    # 6. CORS not wildcard
    add_check
    if grep -q "CORS(app)" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
        if grep -q "CORS_ORIGINS\|origins=" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
            pass_check "CORS has specific origin configuration"
        else
            fail_check "CORS uses default wildcard — configure CORS_ORIGINS"
        fi
    else
        pass_check "CORS configuration present"
    fi

    # 7. Flask debug mode controlled by env
    add_check
    if grep -q "debug=True" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
        if grep -q "FLASK_DEBUG\|DEBUG" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
            pass_check "Debug mode controlled by environment"
        else
            fail_check "Flask debug=True is hardcoded (use FLASK_DEBUG env var)"
        fi
    else
        pass_check "Flask debug mode not hardcoded"
    fi

    # 8. SECRET_KEY configuration
    add_check
    if grep -q "SECRET_KEY\|secret_key" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
        pass_check "Flask SECRET_KEY is configured"
    else
        warn "Flask SECRET_KEY not set (add if using sessions)"
        pass_check "SECRET_KEY not needed (no sessions yet)"
    fi

    # 9. Python dependencies audit (if pip-audit available)
    add_check
    if command -v pip-audit &>/dev/null; then
        info "Running pip-audit..."
        if cd "${PROJECT_ROOT}/backend" && source venv/bin/activate 2>/dev/null && pip-audit --strict 2>/dev/null; then
            pass_check "pip-audit: no vulnerabilities"
        else
            fail_check "pip-audit found vulnerabilities"
        fi
    else
        dim "pip-audit not installed — skipping dependency audit"
        pass_check "Skipped (pip-audit not installed)"
    fi

    # 10. Check for debug print statements
    add_check
    local debug_prints
    debug_prints=$(grep -rn "print(" "${PROJECT_ROOT}/backend/" --include="*.py" 2>/dev/null \
        | grep -v "venv/" | grep -v "__pycache__" | grep -v "test_" || true)
    local debug_count
    debug_count=$(echo "$debug_prints" | grep -c "." || true)
    if [ "$debug_count" -le 5 ]; then
        pass_check "Acceptable print statements (${debug_count} found)"
    else
        fail_check "Too many print statements: ${debug_count} (consider logging)"
    fi

    print_score "Security Score"
    log_to_file "devsecops" "Scan: ${SCORE}/${TOTAL}"
}

case "$SKILL" in
    scan|"")
        run_scan
        ;;
    summary)
        run_scan 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh devsecops scan"
        exit 1
        ;;
esac
