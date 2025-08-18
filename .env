import os
from typing import List, Tuple
from dotenv import load_dotenv

import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

# ------------------------
# Init & Config
# ------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
assert GOOGLE_API_KEY, "Set GOOGLE_API_KEY (env or .env). Do NOT commit secrets."

st.set_page_config(page_title="KMS RAG Chatbot", page_icon="🧭")
st.title("🧭 KMS RAG Chatbot (FAISS)")
st.write(
    "Minimal, fast RAG over your KMS PDFs. Type a question below."
)

# ------------------------
# Caching: load once, reuse
# ------------------------
@st.cache_resource(show_spinner=False)
def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

@st.cache_resource(show_spinner=True)
def get_vectorstore() -> FAISS:
    emb = get_embeddings()
    # allow_dangerous_deserialization is required for FAISS load
    return FAISS.load_local("index_kms", emb, allow_dangerous_deserialization=True)

@st.cache_resource(show_spinner=False)
def get_llm(temperature: float) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature)

# ------------------------
# Sidebar controls
# ------------------------
with st.sidebar:
    st.subheader("Settings")
    top_k: int = st.slider("Top-K chunks", 2, 12, 6)
    temperature: float = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
    show_context: bool = st.checkbox("Show retrieved context", value=True)
    min_score: float = st.slider("Min similarity (0-1)", 0.0, 1.0, 0.0, 0.05)

SYSTEM_PROMPT = (
    "You are a concise compliance/security assistant. "
    "Answer using ONLY the provided context. If the context is insufficient, say: "
    "'No relevant context found.' Keep answers factual and cite the source IDs like [1], [2]."
)

# ------------------------
# Retrieval + Answer
# ------------------------

def build_context_blocks(hits) -> List[str]:
    blocks: List[str] = []
    for i, (doc, score) in enumerate(hits, 1):
        src = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "n/a")
        txt = doc.page_content.strip()
        if not txt:
            continue
        blocks.append(f"[{i}] ({src}, p.{page})\n{txt}")
    return blocks


def truncate_tokens(text: str, max_chars: int = 6000) -> str:
    # Simple char-based truncation to keep prompts light
    return text if len(text) <= max_chars else text[:max_chars]


def answer_query(q: str, k: int, temp: float, min_sim: float) -> Tuple[str, List[Tuple]]:
    vs = get_vectorstore()
    # Use similarity with score and filter low-sim hits if requested
    raw_hits = vs.similarity_search_with_score(q, k=max(k, 8))  # grab a few extra for filtering

    # FAISS returns smaller distance for more similar. Some wrappers convert to score.
    # Here, assume "score" is distance; convert to pseudo-sim in [0,1] by 1/(1+dist)
    filtered = []
    for doc, dist in raw_hits:
        sim = 1.0 / (1.0 + float(dist))
        if sim >= min_sim:
            filtered.append((doc, dist))

    if not filtered:
        return "No relevant context found.", []

    hits = filtered[:k]
    ctx_blocks = build_context_blocks(hits)
    context = truncate_tokens("\n\n".join(ctx_blocks))

    llm = get_llm(temp)
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Question: {q}\n\n"
        f"Context:\n{context}\n\n"
        f"Instructions: cite sources in-line using the IDs in brackets."
    )

    out = llm.invoke(prompt).content
    return out, hits

# ------------------------
# UI
# ------------------------
q = st.text_input("Ask a question (e.g., 'What are FedRAMP authorization stages?')")
if q:
    with st.spinner("Retrieving…"):
        ans, hits = answer_query(q.strip(), top_k, temperature, min_score)
    st.markdown("### Answer")
    st.write(ans)

    if show_context and hits:
        st.markdown("---")
        st.markdown("#### Retrieved context")
        for i, (doc, dist) in enumerate(hits, 1):
            src = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "n/a")
            sim = 1.0 / (1.0 + float(dist))
            with st.expander(f"[{i}] {src}, page {page}  ·  similarity≈{sim:.3f}"):
                st.write(doc.page_content)

st.caption("Tip: keep your .env out of Git. Rotate keys if you accidentally committed them.")