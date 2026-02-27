#!/usr/bin/env bash
# =============================================================================
# utils.sh — Shared utilities for AntiGravity build agents
# =============================================================================

# Project root (parent of agenticAI_skills/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${PROJECT_ROOT}/agenticAI_skills"
LOG_DIR="${SKILLS_DIR}/.logs"

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# Logging helpers
info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[PASS]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail()    { echo -e "${RED}[FAIL]${NC}  $*"; }
header()  { echo -e "\n${BOLD}${PURPLE}=== $* ===${NC}\n"; }
dim()     { echo -e "${DIM}$*${NC}"; }

# Score tracking
SCORE=0
TOTAL=0

add_check() {
    TOTAL=$((TOTAL + 1))
}

pass_check() {
    SCORE=$((SCORE + 1))
    success "$1"
}

fail_check() {
    fail "$1"
}

print_score() {
    local label="${1:-Score}"
    echo ""
    if [ "$SCORE" -eq "$TOTAL" ]; then
        echo -e "${GREEN}${BOLD}${label}: ${SCORE}/${TOTAL}${NC}"
    elif [ "$SCORE" -ge $((TOTAL / 2)) ]; then
        echo -e "${YELLOW}${BOLD}${label}: ${SCORE}/${TOTAL}${NC}"
    else
        echo -e "${RED}${BOLD}${label}: ${SCORE}/${TOTAL}${NC}"
    fi
}

# Check if a command exists
require_cmd() {
    if ! command -v "$1" &>/dev/null; then
        fail "Required command not found: $1"
        return 1
    fi
    return 0
}

# Timestamp for logs
timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Log to file
log_to_file() {
    local agent="$1"
    shift
    echo "[$(timestamp)] $*" >> "${LOG_DIR}/${agent}.log"
}
