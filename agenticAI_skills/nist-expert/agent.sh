#!/usr/bin/env bash
# =============================================================================
# NIST Expert Agent — RAG Validation & Coverage Check
# =============================================================================
# Usage: ./antigravity.sh nist-expert validate
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-validate}"

run_validate() {
    header "NIST Expert Agent — RAG Validation"

    # 1. Check NIST documents exist
    add_check
    local pdf_count
    pdf_count=$(ls "${PROJECT_ROOT}/docs/"*.pdf 2>/dev/null | wc -l | tr -d ' ')
    if [ "$pdf_count" -gt 0 ]; then
        pass_check "Found ${pdf_count} PDF documents in docs/"
    else
        fail_check "No PDF documents in docs/"
    fi

    # 2. Core NIST document present
    add_check
    if [ -f "${PROJECT_ROOT}/docs/nist_80053r5.pdf" ]; then
        pass_check "NIST SP 800-53 Rev.5 present"
    else
        fail_check "NIST SP 800-53 Rev.5 missing (nist_80053r5.pdf)"
    fi

    # 3. FAISS index exists
    add_check
    if [ -f "${PROJECT_ROOT}/index_kms/index.faiss" ] && [ -f "${PROJECT_ROOT}/index_kms/index.pkl" ]; then
        pass_check "FAISS vector index exists (index.faiss + index.pkl)"
    else
        fail_check "FAISS index missing — run 'make ingest'"
    fi

    # 4. FAISS index is non-trivial size
    add_check
    if [ -f "${PROJECT_ROOT}/index_kms/index.faiss" ]; then
        local size_kb
        size_kb=$(du -k "${PROJECT_ROOT}/index_kms/index.faiss" | cut -f1)
        if [ "$size_kb" -gt 100 ]; then
            pass_check "FAISS index is ${size_kb}KB (substantial)"
        else
            fail_check "FAISS index only ${size_kb}KB — may need re-ingestion"
        fi
    else
        fail_check "Cannot check index size (missing)"
    fi

    # 5. RAG engine has proper chunking config
    add_check
    if grep -q "chunk_size=2000" "${PROJECT_ROOT}/backend/ingest.py" 2>/dev/null; then
        pass_check "Chunk size is 2000 (NIST-optimized)"
    else
        fail_check "Non-standard chunk size in ingest.py"
    fi

    # 6. NIST-aware separators configured
    add_check
    if grep -q "Control:" "${PROJECT_ROOT}/backend/ingest.py" 2>/dev/null; then
        pass_check "NIST-aware separators (Control:, Family:) configured"
    else
        fail_check "Missing NIST-specific separators in chunking"
    fi

    # 7. All 5 runtime agents defined
    add_check
    local agent_count
    agent_count=$(grep -c '"name":' "${PROJECT_ROOT}/backend/agents.py" 2>/dev/null || echo 0)
    if [ "$agent_count" -ge 5 ]; then
        pass_check "All ${agent_count} runtime agents defined"
    else
        fail_check "Only ${agent_count} runtime agents (expected 5+)"
    fi

    # 8. Agent routing has keyword fallback
    add_check
    if grep -q "ROUTE_KEYWORDS" "${PROJECT_ROOT}/backend/agents.py" 2>/dev/null; then
        pass_check "Keyword fallback routing configured"
    else
        fail_check "No keyword fallback routing in agents.py"
    fi

    # 9. Source citation in prompts
    add_check
    if grep -q "cite the source" "${PROJECT_ROOT}/backend/agents.py" 2>/dev/null; then
        pass_check "Agent prompts require source citations"
    else
        fail_check "Agent prompts don't enforce citation"
    fi

    # 10. RAG engine returns sources
    add_check
    if grep -q '"sources"' "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null; then
        pass_check "RAG engine returns source citations"
    else
        fail_check "RAG engine doesn't return sources"
    fi

    # List documents
    echo ""
    info "Knowledge Base Contents:"
    for pdf in "${PROJECT_ROOT}/docs/"*.pdf; do
        if [ -f "$pdf" ]; then
            local name size
            name=$(basename "$pdf")
            size=$(du -h "$pdf" | cut -f1)
            dim "  ${name} (${size})"
        fi
    done

    print_score "NIST Coverage Score"
    log_to_file "nist-expert" "Validation: ${SCORE}/${TOTAL}"
}

case "$SKILL" in
    validate|"")
        run_validate
        ;;
    summary)
        run_validate 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh nist-expert validate"
        exit 1
        ;;
esac
