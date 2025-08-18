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

st.set_page_config(page_title="NIST 800-53r5 / CSF 2.0 Chatbot", page_icon="🛡️")
st.title("🛡️ NIST 800-53r5 / CSF 2.0 RAG Chatbot (FAISS)")
st.markdown(
    """
    This private chatbot answers questions **only** from your local PDFs: **NIST SP 800-53 Rev. 5** (security & privacy control catalog) and, if provided, **NIST CSF 2.0** (risk/governance framework). They are **related but distinct**: CSF 2.0 provides Functions/Categories/Outcomes, while 800-53r5 provides detailed controls you can map to those outcomes.

    **How to use**
    1. Put the PDFs in `./docs/` (e.g., `nist_80053r5.pdf`, `NIST_CSF_2.0.pdf`).
    2. Run `python ingest.py` to (re)build the FAISS index.
    3. Ask your question below. The bot cites chunk IDs and shows file/page info in the context panel.

    **Scope**: Security & privacy controls (SP 800-53r5) and CSF 2.0 Functions/Categories (including **Govern**). If a question is outside this scope, you'll see *No relevant context found.*

    **Privacy/Security**: Your PDFs stay local. Only small retrieved snippets are sent to the LLM for answering — never the full documents.
    """
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

SYSTEM_PROMPT = (
    "You are a concise security/compliance assistant. Answer using ONLY the provided context "
    "from NIST SP 800-53 Rev. 5 and/or NIST CSF 2.0. If the context is insufficient, reply: "
    "'No relevant context found.' Keep answers factual and cite the source IDs like [1], [2]."
)

# ------------------------
# Sidebar controls
# ------------------------
with st.sidebar:
    st.subheader("Settings")
    top_k: int = st.slider("Top-K chunks", 2, 12, 6)
    st.caption("Number of chunks retrieved. Higher = more context, slower, and sometimes less focused.")

    temperature: float = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
    st.caption("Output randomness. 0 = deterministic; higher = more creative but less consistent.")

    min_score: float = st.slider("Min similarity (0-1)", 0.0, 1.0, 0.0, 0.05)
    st.caption("Similarity threshold for retrieved chunks. 1.0 = only very close matches; lower = more lenient.")

    with st.sidebar.expander("ℹ️ Help", expanded=False):
        st.write("Re-run `python ingest.py` after you add/replace PDFs in `./docs/`. Use a slightly higher Top-K (6–8) for broad questions.")

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
    return text if len(text) <= max_chars else text[:max_chars]


def answer_query(q: str, k: int, temp: float, min_sim: float) -> Tuple[str, List[Tuple]]:
    vs = get_vectorstore()
    raw_hits = vs.similarity_search_with_score(q, k=max(k, 8))  # grab a few extra for filtering

    # Convert FAISS distance to a pseudo-similarity score
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
    return str(out), hits

# ------------------------
# UI
# ------------------------
q = st.text_input("Ask a question (e.g., 'Which 800-53r5 families cover access control, and how do they align to CSF Protect?')")
if q:
    with st.spinner("Retrieving…"):
        ans, hits = answer_query(q.strip(), top_k, temperature, min_score)
    st.markdown("### Answer")
    st.write(ans)

    if hits:
        st.markdown("---")
        st.markdown("#### Retrieved context")
        for i, (doc, dist) in enumerate(hits, 1):
            src = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "n/a")
            sim = 1.0 / (1.0 + float(dist))
            with st.expander(f"[{i}] {src}, page {page}  ·  similarity≈{sim:.3f}"):
                st.write(doc.page_content)

with st.expander("💡 Starter questions (NIST 800-53r5 + CSF 2.0)", expanded=False):
    st.markdown(
        """
1. **Govern (GV)** → Map CSF 2.0 **Govern** outcomes to **NIST 800-53r5** control families; give 2–3 exemplar controls per outcome.
2. **Protect (PR)** → For a **FIPS 199 Moderate** system, prioritize **AC/IA/SC** controls and justify via **CSF Protect** categories.
3. **Govern/Identify (GV + ID)** → Draft a **POA&M** template aligning **CA/RA** controls to **CSF Govern/Identify**; list minimum evidence fields.
4. **Respond (RS)** → Outline an **IR playbook** linking **CSF Respond** categories to **IR controls** (IR-4, IR-5, IR-8).
5. **Detect/Recover (DE + RC)** → Build an **evidence checklist** for **CM/CP/AU** and show how it supports **CSF Detect/Recover**.
        """
    )

st.markdown("---")
st.markdown("<div style='text-align:center;color:grey'>rudyprasetiya.com | 2025</div>", unsafe_allow_html=True)