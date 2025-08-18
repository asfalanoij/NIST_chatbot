import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
assert GOOGLE_API_KEY, "Set GOOGLE_API_KEY (env or .env)"

# 1) Load PDFs with metadata (file + page)
from langchain_community.document_loaders import PyMuPDFLoader

DOCS_DIR = Path("docs")
pdf_paths = sorted(p for p in DOCS_DIR.glob("*.pdf"))
assert pdf_paths, f"No PDFs found in {DOCS_DIR.resolve()}"

print("PDFs found:")
for p in pdf_paths:
    print(" -", p.name)

docs = []
for p in pdf_paths:
    loader = PyMuPDFLoader(str(p))
    docs.extend(loader.load())

from collections import Counter
_counts = Counter([d.metadata.get("source", "unknown") for d in docs])
for fname, cnt in _counts.items():
    print(f"Loaded {cnt} pages from {Path(fname).name if isinstance(fname, str) else fname}")

print(f"Loaded pages: {len(docs)}")

# 2) Chunk (sane defaults)
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]
)
chunks = splitter.split_documents(docs)
print("Chunks before dedupe:", len(chunks))

# 3) Drop duplicate/empty chunks (policy PDFs repeat a lot)
def _normalize(t: str) -> str:
    return " ".join(t.split())

seen, uniq = set(), []
for d in chunks:
    txt = _normalize(d.page_content)
    if len(txt) < 40:  # skip tiny noise
        continue
    if txt in seen:
        continue
    seen.add(txt)
    uniq.append(d)

chunks = uniq
print("Unique chunks:", len(chunks))

# 4) Embeddings (Google) + cache (so re-runs are instant)
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

base_embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
cache = LocalFileStore("emb_cache")
embeddings = CacheBackedEmbeddings.from_bytes_store(base_embeddings, cache)

# 5) Build FAISS and persist
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

# Determine dimension once via a probe
probe = embeddings.embed_query("sanity")
dim = len(probe)
index = faiss.IndexFlatL2(dim)

vs = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

vs.add_documents(chunks)
Path("index_kms").mkdir(exist_ok=True)
vs.save_local("index_kms")
print("✅ Built & saved FAISS to ./index_kms (with cached embeddings).")