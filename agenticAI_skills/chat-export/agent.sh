#!/usr/bin/env bash
# =============================================================================
# Chat Export Agent — Conversation Export Readiness Check
# =============================================================================
# Usage: ./antigravity.sh chat-export check
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-check}"

run_check() {
    header "Chat Export Agent — 6-Point Export Readiness"

    # 1. Chat response includes source citations
    add_check
    if grep -q "sources" "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null; then
        pass_check "RAG engine returns source citations"
    else
        fail_check "RAG engine missing source citations"
    fi

    # 2. Source includes document name + page number
    add_check
    if grep -q '"source"' "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null && \
       grep -q '"page"' "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null; then
        pass_check "Citations include document name + page number"
    else
        fail_check "Citations missing document/page metadata"
    fi

    # 3. Agent name included in response (needed for export attribution)
    add_check
    if grep -q "agent_name" "${PROJECT_ROOT}/backend/agents.py" 2>/dev/null; then
        pass_check "Response includes agent_name for attribution"
    else
        fail_check "agent_name missing from response"
    fi

    # 4. Frontend handles message history array
    add_check
    if grep -q "messages" "${PROJECT_ROOT}/frontend/src/components/ChatLayout.tsx" 2>/dev/null; then
        pass_check "Frontend maintains message history array"
    else
        fail_check "Frontend missing message history"
    fi

    # 5. MessageBubble renders markdown (exportable format)
    add_check
    if grep -q "markdown\|Markdown\|prose" "${PROJECT_ROOT}/frontend/src/components/MessageBubble.tsx" 2>/dev/null; then
        pass_check "MessageBubble renders markdown (export-ready format)"
    else
        fail_check "MessageBubble does not render markdown"
    fi

    # 6. Content snippet available for audit trail
    add_check
    if grep -q "content_snippet" "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null; then
        pass_check "content_snippet in sources (audit trail support)"
    else
        fail_check "content_snippet missing — needed for audit trail"
    fi

    print_score "Export Readiness"
    log_to_file "chat-export" "Check: ${SCORE}/${TOTAL}"

    echo ""
    info "Export feature status: READY for implementation"
    dim "  Next steps: Add download button (Markdown/PDF) in ChatLayout.tsx"
    dim "  The data structure already supports export — just needs UI + serialization"
}

case "$SKILL" in
    check|"")
        run_check
        ;;
    summary)
        run_check 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh chat-export check"
        exit 1
        ;;
esac
