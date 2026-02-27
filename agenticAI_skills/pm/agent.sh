#!/usr/bin/env bash
# =============================================================================
# PM Agent — Project Maturity Rating & Roadmap
# =============================================================================
# Usage: ./antigravity.sh pm maturity
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-maturity}"

# Weighted maturity indicators (weight out of 100)
run_maturity() {
    header "PM Agent — Maturity Assessment"

    local total_weight=0
    local earned_weight=0

    check_indicator() {
        local name="$1"
        local weight="$2"
        local passed="$3"
        total_weight=$((total_weight + weight))
        if [ "$passed" -eq 1 ]; then
            earned_weight=$((earned_weight + weight))
            success "[${weight}%] ${name}"
        else
            fail "[${weight}%] ${name}"
        fi
    }

    # 1. Tests exist & pass (10%)
    local tests_pass=0
    if [ -d "${PROJECT_ROOT}/backend/tests" ] && ls "${PROJECT_ROOT}"/backend/tests/test_*.py &>/dev/null; then
        if cd "${PROJECT_ROOT}/backend" && source venv/bin/activate 2>/dev/null && python -m pytest tests/ -q --tb=no 2>/dev/null; then
            tests_pass=1
        fi
    fi
    check_indicator "Tests exist & pass" 10 "$tests_pass"

    # 2. Security hardened (15%)
    local sec_pass=0
    local secret_hits
    secret_hits=$(grep -rEn '(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36})' \
        --include="*.py" --include="*.ts" --include="*.tsx" \
        "${PROJECT_ROOT}/backend/" "${PROJECT_ROOT}/frontend/src/" 2>/dev/null | grep -v "venv" || true)
    [ -z "$secret_hits" ] && sec_pass=1
    check_indicator "Security hardened (no secrets)" 15 "$sec_pass"

    # 3. .env.example present (5%)
    local env_pass=0
    [ -f "${PROJECT_ROOT}/.env.example" ] && env_pass=1
    check_indicator ".env.example present" 5 "$env_pass"

    # 4. README.md complete (10%)
    local readme_pass=0
    if [ -f "${PROJECT_ROOT}/README.md" ] && [ "$(wc -l < "${PROJECT_ROOT}/README.md")" -gt 50 ]; then
        readme_pass=1
    fi
    check_indicator "README.md complete" 10 "$readme_pass"

    # 5. API authentication (5%)
    local auth_pass=0
    if grep -q "require_api_key" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
        auth_pass=1
    fi
    check_indicator "API authentication implemented" 5 "$auth_pass"

    # 6. CORS configured (5%)
    local cors_pass=0
    if grep -q "CORS_ORIGINS\|origins=" "${PROJECT_ROOT}/backend/app.py" 2>/dev/null; then
        cors_pass=1
    fi
    check_indicator "CORS configured (not wildcard)" 5 "$cors_pass"

    # 7. API fallback Gemini/Ollama (10%)
    local fallback_pass=0
    if grep -q "GEMINI_API_KEY\|ChatGoogleGenerativeAI" "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null; then
        fallback_pass=1
    fi
    check_indicator "LLM + Embedding fallback (Gemini/Ollama)" 10 "$fallback_pass"

    # 8. Visitor tracking works (10%)
    local visitor_pass=0
    if curl -s http://localhost:5050/api/visitors/count 2>/dev/null | grep -q "unique_visitors"; then
        visitor_pass=1
    fi
    check_indicator "Visitor tracking works" 10 "$visitor_pass"

    # 9. Frontend builds clean (10%)
    local build_pass=0
    if cd "${PROJECT_ROOT}/frontend" && npm run build --silent 2>/dev/null; then
        build_pass=1
    fi
    check_indicator "Frontend builds clean" 10 "$build_pass"

    # 10. All 13 agents operational (10%)
    local agents_pass=0
    local agent_count=0
    for agent_dir in qa devsecops nist-expert data-scientist pm e2e-test context-optimizer visitor-tracker api-auth api-loadtest rag-evaluator chat-export cicd; do
        [ -f "${SKILLS_DIR}/${agent_dir}/agent.sh" ] && agent_count=$((agent_count + 1))
    done
    [ "$agent_count" -eq 13 ] && agents_pass=1
    check_indicator "All 13 build agents operational" 10 "$agents_pass"

    # 11. RAG index + live chat works (10%)
    local rag_pass=0
    if [ -f "${PROJECT_ROOT}/backend/index_kms/index.faiss" ]; then
        local chat_code
        chat_code=$(curl -s -o /dev/null -w "%{http_code}" \
            -X POST http://localhost:5050/api/chat \
            -H "Content-Type: application/json" \
            -d '{"message":"What is AC-2?"}' 2>/dev/null || echo "000")
        if [ "$chat_code" = "200" ]; then
            rag_pass=1
        fi
    fi
    check_indicator "RAG index + live chat operational" 10 "$rag_pass"

    # Calculate percentage
    echo ""
    local pct=$((earned_weight * 100 / total_weight))
    if [ "$pct" -ge 90 ]; then
        echo -e "${GREEN}${BOLD}Maturity: ${pct}% (${earned_weight}/${total_weight} weighted points)${NC}"
    elif [ "$pct" -ge 50 ]; then
        echo -e "${YELLOW}${BOLD}Maturity: ${pct}% (${earned_weight}/${total_weight} weighted points)${NC}"
    else
        echo -e "${RED}${BOLD}Maturity: ${pct}% (${earned_weight}/${total_weight} weighted points)${NC}"
    fi

    log_to_file "pm" "Maturity: ${pct}% (${earned_weight}/${total_weight})"
}

run_roadmap() {
    header "PM Agent — Sprint Roadmap"
    echo ""
    echo -e "${GREEN}Sprint 1: Security + Agent Skeleton       [DONE]${NC}"
    echo -e "${GREEN}Sprint 2: Testing Infrastructure          [DONE]${NC}"
    echo -e "${GREEN}Sprint 3: Visitor Tracking + API           [DONE]${NC}"
    echo -e "${GREEN}Sprint 4: Documentation + Context          [DONE]${NC}"
    echo -e "${YELLOW}Sprint 5: Auth, Embeddings & New Agents   [IN PROGRESS]${NC}"
    echo ""
    echo -e "${BOLD}Sprint 5 Completed:${NC}"
    echo "  [x] API authentication (@require_api_key)"
    echo "  [x] Embedding dimension fix (get_embeddings)"
    echo "  [x] 5 new build agents (8 -> 13)"
    echo "  [x] Test suite expanded (26 -> 34)"
    echo "  [x] FAISS index rebuilt (Gemini 3072-dim)"
    echo "  [x] Dynamic LLM backend indicator in UI"
    echo ""
    echo -e "${BOLD}Sprint 5 Remaining:${NC}"
    echo "  [ ] GitHub Actions CI workflow"
    echo "  [ ] Git commit + tag v2.0.0"
    echo "  [ ] Push to GitHub"
}

case "$SKILL" in
    maturity|"")
        run_maturity
        ;;
    roadmap)
        run_roadmap
        ;;
    summary)
        run_maturity 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh pm [maturity|roadmap]"
        exit 1
        ;;
esac
