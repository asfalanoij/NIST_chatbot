#!/usr/bin/env bash
# =============================================================================
# Visitor Tracker Agent — Visitor Tracking Health Check
# =============================================================================
# Usage: ./antigravity.sh visitor-tracker status
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-status}"

run_status() {
    header "Visitor Tracker Agent — Status"

    # 1. Check visitor_tracker.py exists
    add_check
    if [ -f "${PROJECT_ROOT}/backend/visitor_tracker.py" ]; then
        pass_check "visitor_tracker.py exists"
    else
        fail_check "visitor_tracker.py missing"
    fi

    # 2. Check SQLite database exists
    add_check
    if ls "${PROJECT_ROOT}/backend/"*.db &>/dev/null 2>&1; then
        local db_file
        db_file=$(ls "${PROJECT_ROOT}/backend/"*.db 2>/dev/null | head -1)
        local db_size
        db_size=$(du -h "$db_file" | cut -f1)
        pass_check "SQLite database exists (${db_size})"
    else
        fail_check "No SQLite database found (tracking not started yet)"
    fi

    # 3. Check /api/visitors/count endpoint
    add_check
    local response
    response=$(curl -s --max-time 5 http://localhost:5050/api/visitors/count 2>/dev/null || echo "")
    if echo "$response" | grep -q "unique_visitors"; then
        pass_check "/api/visitors/count endpoint responds"
        local unique total
        unique=$(echo "$response" | python3 -c "import json,sys; print(json.load(sys.stdin)['unique_visitors'])" 2>/dev/null || echo "?")
        total=$(echo "$response" | python3 -c "import json,sys; print(json.load(sys.stdin)['total_visits'])" 2>/dev/null || echo "?")
        info "  Unique visitors: ${unique}"
        info "  Total visits: ${total}"
    else
        fail_check "/api/visitors/count not responding"
    fi

    # 4. Check @before_request is wired in app.py
    add_check
    if grep -q "before_request\|track_visitor" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
        pass_check "Visitor tracking hooked into Flask"
    else
        fail_check "Visitor tracking not wired in app.py"
    fi

    # 5. Check *.db is gitignored
    add_check
    if grep -q "\*.db" "${PROJECT_ROOT}/.gitignore" 2>/dev/null; then
        pass_check "*.db is in .gitignore"
    else
        fail_check "*.db not in .gitignore (SQLite database may be committed)"
    fi

    print_score "Visitor Tracker Score"
    log_to_file "visitor-tracker" "Status: ${SCORE}/${TOTAL}"
}

case "$SKILL" in
    status|"")
        run_status
        ;;
    summary)
        run_status 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh visitor-tracker status"
        exit 1
        ;;
esac
