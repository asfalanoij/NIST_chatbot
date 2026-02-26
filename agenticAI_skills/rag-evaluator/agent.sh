#!/usr/bin/env bash
# =============================================================================
# RAG Evaluator Agent — Retrieval Quality & Embedding Health
# =============================================================================
# Usage: ./antigravity.sh rag-evaluator evaluate
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-evaluate}"
API_BASE="${API_BASE:-http://localhost:5050}"

# Test queries with expected keywords in the answer
# Format: "query|expected_keyword1,expected_keyword2"
TEST_CASES=(
    "What is AC-2 Account Management?|AC-2,account"
    "Explain FIPS 199 security categorization|FIPS,categorization,impact"
    "What are the RMF steps?|categorize,select,implement,assess,authorize,monitor"
    "How does FedRAMP relate to NIST 800-53?|FedRAMP,800-53"
    "What evidence artifacts are needed for an audit?|evidence,artifact"
)

run_evaluate() {
    header "RAG Evaluator — Retrieval Quality Assessment"

    # 1. FAISS index exists
    add_check
    if [ -f "${PROJECT_ROOT}/backend/index_kms/index.faiss" ]; then
        local index_size
        index_size=$(du -h "${PROJECT_ROOT}/backend/index_kms/index.faiss" 2>/dev/null | awk '{print $1}')
        pass_check "FAISS index exists (${index_size})"
    else
        fail_check "FAISS index missing — run: make ingest"
        print_score "RAG Score"
        log_to_file "rag-evaluator" "Evaluate: FAISS index missing"
        return
    fi

    # 2. Pickle metadata file exists
    add_check
    if [ -f "${PROJECT_ROOT}/backend/index_kms/index.pkl" ]; then
        pass_check "Index metadata (index.pkl) exists"
    else
        fail_check "Index metadata missing"
    fi

    # 3. get_embeddings() function exists (unified embedding strategy)
    add_check
    if grep -q "def get_embeddings" "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null; then
        pass_check "get_embeddings() function present (unified embedding strategy)"
    else
        fail_check "get_embeddings() missing — embedding mismatch risk"
    fi

    # 4. Ingest uses get_embeddings (not hardcoded)
    add_check
    if grep -q "get_embeddings" "${PROJECT_ROOT}/backend/ingest.py" 2>/dev/null; then
        if grep -q "OllamaEmbeddings" "${PROJECT_ROOT}/backend/ingest.py" 2>/dev/null; then
            fail_check "ingest.py still has hardcoded OllamaEmbeddings"
        else
            pass_check "ingest.py uses get_embeddings() (no hardcoded embeddings)"
        fi
    else
        fail_check "ingest.py does not use get_embeddings()"
    fi

    # 5. Embedding tests exist
    add_check
    if grep -q "TestGetEmbeddings" "${PROJECT_ROOT}/backend/tests/test_rag_engine.py" 2>/dev/null; then
        pass_check "Embedding tests exist (TestGetEmbeddings)"
    else
        fail_check "No embedding tests found"
    fi

    # 6. Source docs present for ingestion
    add_check
    local pdf_count
    pdf_count=$(ls "${PROJECT_ROOT}/docs/"*.pdf 2>/dev/null | wc -l | tr -d ' ')
    if [ "$pdf_count" -gt 0 ]; then
        pass_check "Source documents present (${pdf_count} PDFs in docs/)"
    else
        fail_check "No PDFs in docs/ directory"
    fi

    # 7-11. Live retrieval quality tests (if backend running)
    local health_resp
    health_resp=$(curl -s -o /dev/null -w "%{http_code}" "${API_BASE}/api/health" 2>/dev/null || echo "000")

    if [ "$health_resp" = "200" ]; then
        info "Backend running — executing ${#TEST_CASES[@]} retrieval quality tests..."
        echo ""

        local auth_header=""
        if [ -n "${API_KEY:-}" ]; then
            auth_header="-H X-API-Key:${API_KEY}"
        fi

        for tc in "${TEST_CASES[@]}"; do
            add_check
            local query expected_str
            query="${tc%%|*}"
            expected_str="${tc##*|}"

            # Query the API
            local response
            response=$(curl -s -X POST "${API_BASE}/api/chat" \
                -H "Content-Type: application/json" \
                ${auth_header} \
                -d "{\"message\":\"${query}\"}" 2>/dev/null || echo '{"error":"timeout"}')

            # Check for expected keywords in answer
            local answer
            answer=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin).get('answer',''))" 2>/dev/null || echo "")
            local sources
            sources=$(echo "$response" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('sources',[])))" 2>/dev/null || echo "0")

            if [ -z "$answer" ]; then
                fail_check "Query: '${query}' — no answer returned"
                continue
            fi

            # Check if expected keywords appear in answer (case insensitive)
            local answer_lower
            answer_lower=$(echo "$answer" | tr '[:upper:]' '[:lower:]')
            local found=0
            local total_expected=0
            IFS=',' read -ra expected_arr <<< "$expected_str"
            for kw in "${expected_arr[@]}"; do
                total_expected=$((total_expected + 1))
                local kw_lower
                kw_lower=$(echo "$kw" | tr '[:upper:]' '[:lower:]')
                if echo "$answer_lower" | grep -q "$kw_lower"; then
                    found=$((found + 1))
                fi
            done

            local hit_rate=$((found * 100 / total_expected))
            if [ "$hit_rate" -ge 50 ] && [ "$sources" -gt 0 ]; then
                pass_check "Query: '${query:0:40}...' — ${found}/${total_expected} keywords, ${sources} sources"
            else
                fail_check "Query: '${query:0:40}...' — ${found}/${total_expected} keywords, ${sources} sources"
            fi
        done
    else
        dim "Backend not running — skipping ${#TEST_CASES[@]} live retrieval tests"
        for tc in "${TEST_CASES[@]}"; do
            add_check
            pass_check "Skipped (backend not running)"
        done
    fi

    print_score "RAG Score"
    log_to_file "rag-evaluator" "Evaluate: ${SCORE}/${TOTAL}"
}

case "$SKILL" in
    evaluate|"")
        run_evaluate
        ;;
    summary)
        run_evaluate 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh rag-evaluator evaluate"
        exit 1
        ;;
esac
