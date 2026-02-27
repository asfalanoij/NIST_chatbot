#!/usr/bin/env bash
# =============================================================================
# antigravity.sh — AntiGravity Build Agent Dispatcher
# =============================================================================
# Usage: ./antigravity.sh <agent> <skill>
# Example: ./antigravity.sh qa inspect
#          ./antigravity.sh devsecops scan
#          ./antigravity.sh pm maturity
#          ./antigravity.sh help
# =============================================================================

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/utils.sh"

# All agent names (order matters for display)
ALL_AGENTS="qa devsecops nist-expert data-scientist pm e2e-test context-optimizer visitor-tracker api-auth api-loadtest rag-evaluator chat-export cicd"

# Get agent description
agent_desc() {
    case "$1" in
        qa)                 echo "16-point quality inspection" ;;
        devsecops)          echo "Security scanning & .gitignore audit" ;;
        nist-expert)        echo "RAG validation & NIST coverage" ;;
        data-scientist)     echo "Embedding profile & chunk analysis" ;;
        pm)                 echo "Project maturity % & roadmap" ;;
        e2e-test)           echo "Test orchestration (backend + frontend)" ;;
        context-optimizer)  echo "Token analysis & context report" ;;
        visitor-tracker)    echo "Visitor tracking health check" ;;
        api-auth)           echo "Authentication & authorization verification" ;;
        api-loadtest)       echo "Endpoint stress testing & latency" ;;
        rag-evaluator)      echo "Retrieval quality & embedding health" ;;
        chat-export)        echo "Conversation export readiness" ;;
        cicd)               echo "CI/CD pipeline readiness check" ;;
        *)                  echo "Unknown agent" ;;
    esac
}

# Validate agent name
is_valid_agent() {
    case "$1" in
        qa|devsecops|nist-expert|data-scientist|pm|e2e-test|context-optimizer|visitor-tracker|api-auth|api-loadtest|rag-evaluator|chat-export|cicd)
            return 0 ;;
        *)
            return 1 ;;
    esac
}

show_help() {
    header "AntiGravity Build Agents"
    echo -e "${BOLD}Usage:${NC} ./antigravity.sh <agent> <skill>"
    echo ""
    echo -e "${BOLD}Available Agents:${NC}"
    echo ""
    for agent in $ALL_AGENTS; do
        printf "  ${CYAN}%-20s${NC} %s\n" "$agent" "$(agent_desc "$agent")"
    done
    echo ""
    echo -e "${BOLD}Examples:${NC}"
    echo "  ./antigravity.sh qa inspect"
    echo "  ./antigravity.sh devsecops scan"
    echo "  ./antigravity.sh pm maturity"
    echo "  ./antigravity.sh api-auth verify"
    echo "  ./antigravity.sh rag-evaluator evaluate"
    echo "  ./antigravity.sh cicd check"
    echo "  ./antigravity.sh all"
    echo ""
}

run_all() {
    header "Running All Agents"
    for agent in $ALL_AGENTS; do
        local agent_script="${SCRIPT_DIR}/${agent}/agent.sh"
        if [ -f "$agent_script" ]; then
            echo -e "\n${BOLD}--- ${agent} ---${NC}"
            bash "$agent_script" "summary" 2>&1 || true
        fi
    done
}

# Main dispatch
AGENT="${1:-help}"
SKILL="${2:-}"

if [ "$AGENT" = "help" ] || [ "$AGENT" = "--help" ] || [ "$AGENT" = "-h" ]; then
    show_help
    exit 0
fi

if [ "$AGENT" = "all" ]; then
    run_all
    exit 0
fi

# Validate agent
if ! is_valid_agent "$AGENT"; then
    fail "Unknown agent: $AGENT"
    echo ""
    show_help
    exit 1
fi

# Find and run agent script
AGENT_SCRIPT="${SCRIPT_DIR}/${AGENT}/agent.sh"

if [ ! -f "$AGENT_SCRIPT" ]; then
    fail "Agent script not found: ${AGENT_SCRIPT}"
    exit 1
fi

# Log invocation
log_to_file "$AGENT" "Invoked: $AGENT $SKILL"

# Execute
bash "$AGENT_SCRIPT" "$SKILL"
