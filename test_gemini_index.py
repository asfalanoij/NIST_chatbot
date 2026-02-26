
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def test():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No GEMINI_API_KEY found.")
        return

    print("Loading index with Gemini Embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=api_key)
    
    try:
        # Try loading the index in backend/index_kms
        index_path = "backend/index_kms"
        if not os.path.exists(index_path):
             print(f"Index not found at {index_path}")
             return

        vector_store = FAISS.load_local(
            index_path, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        
        print(f"FAISS Index dimension: {vector_store.index.d}")
        
        test_emb = embeddings.embed_query("test")
        print(f"Gemini Embedding dimension: {len(test_emb)}")

        print("Index loaded. Querying 'security controls'...")
        results = vector_store.similarity_search("security controls", k=1)
        
        if results:
            print(f"Result: {results[0].page_content[:200]}...")
            print("SUCCESS: Index compatible.")
        else:
            print("No results returned.")

    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test()

