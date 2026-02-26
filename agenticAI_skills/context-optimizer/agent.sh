#!/usr/bin/env bash
# =============================================================================
# Context Optimizer Agent — Token Analysis & Context Report
# =============================================================================
# Usage: ./antigravity.sh context-optimizer report
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-report}"

count_lines() {
    local path="$1"
    local pattern="${2:-*}"
    find "$path" -name "$pattern" -not -path "*/venv/*" -not -path "*/node_modules/*" -not -path "*/__pycache__/*" -not -path "*/.git/*" -not -path "*/dist/*" -type f 2>/dev/null | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}'
}

run_report() {
    header "Context Optimizer — Token Analysis Report"

    # Backend code stats
    info "Backend (Python):"
    local py_lines
    py_lines=$(count_lines "${PROJECT_ROOT}/backend" "*.py")
    dim "  Total lines: ${py_lines:-0}"
    echo ""

    info "Key files:"
    for f in app.py rag_engine.py agents.py ingest.py; do
        if [ -f "${PROJECT_ROOT}/backend/${f}" ]; then
            local lines
            lines=$(wc -l < "${PROJECT_ROOT}/backend/${f}" | tr -d ' ')
            dim "  backend/${f}: ${lines} lines (~$((lines * 4)) tokens est.)"
        fi
    done

    # Frontend code stats
    echo ""
    info "Frontend (TypeScript/React):"
    local ts_lines
    ts_lines=$(count_lines "${PROJECT_ROOT}/frontend/src" "*.tsx")
    ts_lines="${ts_lines:-0}"
    dim "  Total .tsx lines: ${ts_lines}"

    for f in "${PROJECT_ROOT}/frontend/src/components/"*.tsx; do
        if [ -f "$f" ]; then
            local name lines
            name=$(basename "$f")
            lines=$(wc -l < "$f" | tr -d ' ')
            dim "  components/${name}: ${lines} lines (~$((lines * 4)) tokens est.)"
        fi
    done

    # Agent scripts stats
    echo ""
    info "Build Agents (Shell):"
    local sh_lines=0
    for agent_dir in qa devsecops nist-expert data-scientist pm e2e-test context-optimizer visitor-tracker; do
        local f="${SKILLS_DIR}/${agent_dir}/agent.sh"
        if [ -f "$f" ]; then
            local lines
            lines=$(wc -l < "$f" | tr -d ' ')
            sh_lines=$((sh_lines + lines))
            dim "  ${agent_dir}/agent.sh: ${lines} lines"
        fi
    done
    dim "  Total agent lines: ${sh_lines}"

    # Context files
    echo ""
    info "Context System:"
    for f in MEMORY.md context_map.md; do
        local path="${SKILLS_DIR}/${f}"
        if [ -f "$path" ]; then
            local lines
            lines=$(wc -l < "$path" | tr -d ' ')
            dim "  ${f}: ${lines} lines (~$((lines * 4)) tokens est.)"
        else
            dim "  ${f}: not found"
        fi
    done

    # Total project estimate
    echo ""
    info "Estimated Total Context Cost:"
    local total_lines=$((${py_lines:-0} + ${ts_lines:-0} + sh_lines))
    local total_tokens=$((total_lines * 4))
    dim "  ~${total_lines} lines of code"
    dim "  ~${total_tokens} tokens (rough estimate at 4 tokens/line)"

    echo ""
    success "Report complete"
    log_to_file "context-optimizer" "Report generated: ~${total_tokens} tokens"
}

case "$SKILL" in
    report|"")
        run_report
        ;;
    summary)
        run_report 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh context-optimizer report"
        exit 1
        ;;
esac
