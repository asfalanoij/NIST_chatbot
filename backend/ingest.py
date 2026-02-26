import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from rag_engine import get_embeddings

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "index_kms")

def ingest_documents():
    """
    Ingests all PDF documents from the docs/ directory.
    """
    print(f"Scanning for documents in {DOCS_DIR}...")
    pdf_files = glob.glob(os.path.join(DOCS_DIR, "*.pdf"))
    
    if not pdf_files:
        return {"status": "no_files", "message": "No PDF files found in docs/ directory."}

    all_splits = []
    
    # "Deep Analysis" Chunking Strategy
    # NIST documents have specific structures. We want to keep control families together if possible.
    # We use a large chunk size with overlap to capture context.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        separators=["\n\n", "\n", "Family:", "Control:", "(", " "]
    )

    for pdf_path in pdf_files:
        print(f"Processing {pdf_path}...")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        splits = text_splitter.split_documents(docs)
        
        # Add metadata
        for split in splits:
            split.metadata["source"] = os.path.basename(pdf_path)
        
        all_splits.extend(splits)
        print(f"  - Generated {len(splits)} chunks.")

    if not all_splits:
        return {"status": "empty", "message": "Documents were empty or could not be read."}

    print("Generating embeddings (this may take a while)...")
    embeddings = get_embeddings()  # Must match RAG Engine
    
    vector_store = FAISS.from_documents(all_splits, embeddings)
    vector_store.save_local(INDEX_PATH)
    
    print(f" Index saved to {INDEX_PATH}")
    
    return {
        "status": "success", 
        "total_documents": len(pdf_files),
        "total_chunks": len(all_splits),
        "index_path": INDEX_PATH
    }

if __name__ == "__main__":
    ingest_documents()
