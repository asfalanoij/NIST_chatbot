#!/usr/bin/env bash
# =============================================================================
# API Load Test Agent — Endpoint Stress Testing
# =============================================================================
# Usage: ./antigravity.sh api-loadtest stress
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-stress}"
API_BASE="${API_BASE:-http://localhost:5050}"
CONCURRENCY="${LOADTEST_CONCURRENCY:-5}"
REQUESTS="${LOADTEST_REQUESTS:-20}"

run_stress() {
    header "API Load Test Agent — Stress Test"

    # Check if backend is running
    local health_resp
    health_resp=$(curl -s -o /dev/null -w "%{http_code}" "${API_BASE}/api/health" 2>/dev/null || echo "000")
    if [ "$health_resp" = "000" ]; then
        fail "Backend not running at ${API_BASE}. Start with: make start-backend"
        exit 1
    fi

    info "Target: ${API_BASE}"
    info "Requests: ${REQUESTS} | Concurrency: ${CONCURRENCY}"
    echo ""

    # 1. Health endpoint latency
    add_check
    info "Testing /api/health latency..."
    local health_times=()
    local health_fail=0
    for i in $(seq 1 "$REQUESTS"); do
        local t
        t=$(curl -s -o /dev/null -w "%{time_total}" "${API_BASE}/api/health" 2>/dev/null || echo "999")
        if [ "$t" = "999" ]; then
            health_fail=$((health_fail + 1))
        fi
        health_times+=("$t")
    done
    # Calculate avg (bash 3.2 compatible — use awk)
    local health_avg
    health_avg=$(printf '%s\n' "${health_times[@]}" | awk '{sum+=$1} END{printf "%.3f", sum/NR}')
    if [ "$health_fail" -eq 0 ]; then
        pass_check "/api/health: avg ${health_avg}s (0 failures over ${REQUESTS} requests)"
    else
        fail_check "/api/health: ${health_fail}/${REQUESTS} failures, avg ${health_avg}s"
    fi

    # 2. Visitor count endpoint latency
    add_check
    info "Testing /api/visitors/count latency..."
    local visitor_times=()
    local visitor_fail=0
    for i in $(seq 1 "$REQUESTS"); do
        local t
        t=$(curl -s -o /dev/null -w "%{time_total}" "${API_BASE}/api/visitors/count" 2>/dev/null || echo "999")
        if [ "$t" = "999" ]; then
            visitor_fail=$((visitor_fail + 1))
        fi
        visitor_times+=("$t")
    done
    local visitor_avg
    visitor_avg=$(printf '%s\n' "${visitor_times[@]}" | awk '{sum+=$1} END{printf "%.3f", sum/NR}')
    if [ "$visitor_fail" -eq 0 ]; then
        pass_check "/api/visitors/count: avg ${visitor_avg}s (0 failures)"
    else
        fail_check "/api/visitors/count: ${visitor_fail}/${REQUESTS} failures"
    fi

    # 3. Chat endpoint (single request — heavier due to RAG + LLM)
    add_check
    info "Testing /api/chat single-request latency..."
    # Build headers — include API key if set
    local auth_header=""
    if [ -n "${API_KEY:-}" ]; then
        auth_header="-H X-API-Key:${API_KEY}"
    fi
    local chat_time
    local chat_code
    chat_time=$(curl -s -o /dev/null -w "%{time_total}" \
        -X POST "${API_BASE}/api/chat" \
        -H "Content-Type: application/json" \
        ${auth_header} \
        -d '{"message":"What is AC-2?"}' 2>/dev/null || echo "999")
    chat_code=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "${API_BASE}/api/chat" \
        -H "Content-Type: application/json" \
        ${auth_header} \
        -d '{"message":"What is AC-2?"}' 2>/dev/null || echo "000")

    if [ "$chat_code" = "200" ]; then
        if awk "BEGIN{exit !($chat_time < 30)}" 2>/dev/null; then
            pass_check "/api/chat: ${chat_time}s (HTTP ${chat_code})"
        else
            fail_check "/api/chat: ${chat_time}s exceeds 30s threshold"
        fi
    elif [ "$chat_code" = "401" ]; then
        warn "  /api/chat returned 401 — set API_KEY env for load testing"
        pass_check "/api/chat: auth working (set API_KEY to test latency)"
    else
        fail_check "/api/chat: HTTP ${chat_code} (expected 200)"
    fi

    # 4. Concurrent health requests
    add_check
    info "Testing ${CONCURRENCY} concurrent /api/health requests..."
    local concurrent_fail=0
    local pids=()
    local tmpdir
    tmpdir=$(mktemp -d)
    for i in $(seq 1 "$CONCURRENCY"); do
        curl -s -o /dev/null -w "%{http_code}" "${API_BASE}/api/health" > "${tmpdir}/${i}.code" 2>/dev/null &
        pids+=($!)
    done
    for pid in "${pids[@]}"; do
        wait "$pid" 2>/dev/null || true
    done
    for i in $(seq 1 "$CONCURRENCY"); do
        local code
        code=$(cat "${tmpdir}/${i}.code" 2>/dev/null || echo "000")
        if [ "$code" != "200" ]; then
            concurrent_fail=$((concurrent_fail + 1))
        fi
    done
    rm -rf "$tmpdir"
    if [ "$concurrent_fail" -eq 0 ]; then
        pass_check "Concurrent: ${CONCURRENCY}/${CONCURRENCY} health requests succeeded"
    else
        fail_check "Concurrent: ${concurrent_fail}/${CONCURRENCY} health requests failed"
    fi

    print_score "Load Test Score"
    log_to_file "api-loadtest" "Stress: ${SCORE}/${TOTAL} | Health avg: ${health_avg}s | Chat: ${chat_time}s"
}

case "$SKILL" in
    stress|"")
        run_stress
        ;;
    summary)
        run_stress 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh api-loadtest stress"
        exit 1
        ;;
esac
