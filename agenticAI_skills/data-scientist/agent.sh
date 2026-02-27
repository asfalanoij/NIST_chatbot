#!/usr/bin/env bash
# =============================================================================
# Data Scientist Agent — Embedding Profile & Chunk Analysis
# =============================================================================
# Usage: ./antigravity.sh data-scientist profile
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${SCRIPT_DIR}/utils.sh"

SKILL="${1:-profile}"

run_profile() {
    header "Data Scientist Agent — Embedding Profile"

    # Document stats
    info "Source Documents:"
    local total_pdf_size=0
    for pdf in "${PROJECT_ROOT}/docs/"*.pdf; do
        if [ -f "$pdf" ]; then
            local name size_bytes
            name=$(basename "$pdf")
            size_bytes=$(stat -f%z "$pdf" 2>/dev/null || stat -c%s "$pdf" 2>/dev/null || echo 0)
            total_pdf_size=$((total_pdf_size + size_bytes))
            local size_mb
            size_mb=$(echo "scale=1; $size_bytes / 1048576" | bc 2>/dev/null || echo "?")
            dim "  ${name}: ${size_mb}MB"
        fi
    done
    local total_mb
    total_mb=$(echo "scale=1; $total_pdf_size / 1048576" | bc 2>/dev/null || echo "?")
    info "Total document size: ${total_mb}MB"

    # Embedding cache stats
    echo ""
    info "Embedding Cache:"
    if [ -d "${PROJECT_ROOT}/emb_cache" ]; then
        local cache_files cache_size
        cache_files=$(find "${PROJECT_ROOT}/emb_cache" -type f | wc -l | tr -d ' ')
        cache_size=$(du -sh "${PROJECT_ROOT}/emb_cache" 2>/dev/null | cut -f1)
        dim "  Files: ${cache_files}"
        dim "  Size: ${cache_size}"
    else
        dim "  No embedding cache found"
    fi

    # FAISS index stats
    echo ""
    info "FAISS Vector Index:"
    if [ -f "${PROJECT_ROOT}/index_kms/index.faiss" ]; then
        local idx_size pkl_size
        idx_size=$(du -h "${PROJECT_ROOT}/index_kms/index.faiss" | cut -f1)
        pkl_size=$(du -h "${PROJECT_ROOT}/index_kms/index.pkl" | cut -f1)
        dim "  index.faiss: ${idx_size}"
        dim "  index.pkl: ${pkl_size}"
    else
        warn "  No FAISS index found"
    fi

    # Chunking configuration
    echo ""
    info "Chunking Configuration (from ingest.py):"
    local chunk_size chunk_overlap
    chunk_size=$(grep "chunk_size" "${PROJECT_ROOT}/backend/ingest.py" 2>/dev/null | head -1 | grep -oE '[0-9]+' || echo "unknown")
    chunk_overlap=$(grep "chunk_overlap" "${PROJECT_ROOT}/backend/ingest.py" 2>/dev/null | head -1 | grep -oE '[0-9]+' || echo "unknown")
    dim "  chunk_size: ${chunk_size}"
    dim "  chunk_overlap: ${chunk_overlap}"

    # Embedding model
    echo ""
    info "Embedding Model:"
    local emb_model
    emb_model=$(grep "OllamaEmbeddings" "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null | grep -oE 'model="[^"]*"' | head -1 || echo "unknown")
    dim "  ${emb_model}"

    # LLM model
    info "LLM Model:"
    local llm_model
    llm_model=$(grep "ChatOllama\|ChatGoogleGenerativeAI" "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null | grep -oE 'model="[^"]*"' | head -1 || echo "unknown")
    dim "  ${llm_model}"

    # Retrieval config
    echo ""
    info "Retrieval Configuration (from rag_engine.py):"
    local top_k
    top_k=$(grep "similarity_search" "${PROJECT_ROOT}/backend/rag_engine.py" 2>/dev/null | grep -oE 'k=[0-9]+' || echo "k=unknown")
    dim "  top_k: ${top_k}"

    echo ""
    success "Profile complete"
    log_to_file "data-scientist" "Profile generated"
}

case "$SKILL" in
    profile|"")
        run_profile
        ;;
    summary)
        run_profile 2>/dev/null
        ;;
    *)
        echo "Usage: ./antigravity.sh data-scientist profile"
        exit 1
        ;;
esac
