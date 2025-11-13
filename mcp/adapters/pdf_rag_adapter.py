import requests
import pymupdf  # PDF text extraction
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# Initialize expensive components once
print("[Tool: PDF_RAG] Initializing components (Embeddings, Splitter)...")
embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
print("[Tool: PDF_RAG] Components ready.")


def pdf_rag_query(url: str, query: str, include_images: bool = False) -> list:
    """
    Performs a full RAG workflow on a live PDF URL.
    Updated to match the unified adapter return format:
    
    Returns:
    [
      {
        "title": "PDF Snippet",
        "url": <pdf_url>,
        "content": "Relevant text here...",
        "source": "pdf_rag",
        "images": []
      }
    ]
    """
    print(f"\n[Tool: PDF_RAG] Starting RAG for URL: {url}")

    try:
        # 1. Download PDF
        print("[Tool: PDF_RAG] Downloading PDF...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # 2. Extract text
        print("[Tool: PDF_RAG] Extracting text from PDF...")
        with pymupdf.open("pdf", response.content) as doc:
            full_text = "".join(page.get_text() for page in doc)

        if not full_text.strip():
            print("[Tool: PDF_RAG] No text extracted.")
            return [{
                "title": "PDF Snippet",
                "url": url,
                "content": "ERROR: No text extracted from PDF.",
                "source": "pdf_rag",
                "images": []
            }]

        # 3. Chunk text
        print(f"[Tool: PDF_RAG] Splitting {len(full_text)} chars into chunks...")
        chunks = text_splitter.split_text(full_text)

        # 4. Embed + Create Vector Store
        print(f"[Tool: PDF_RAG] Creating vector store with {len(chunks)} chunks...")
        vector_store = Chroma.from_texts(texts=chunks, embedding=embeddings_model)

        # 5. Retrieve relevant chunks
        print(f"[Tool: PDF_RAG] Querying vector store for: {query}")
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(query)

        if not relevant_docs:
            return [{
                "title": "PDF Snippet",
                "url": url,
                "content": "No relevant text found for query.",
                "source": "pdf_rag",
                "images": []
            }]

        # 6. Format into unified structure
        results = []
        for doc in relevant_docs:
            results.append({
                "title": "PDF Snippet",
                "url": url,
                "content": doc.page_content[:2000],  # Keep reasonable size
                "source": "pdf_rag",
                "images": []
            })

        print("[Tool: PDF_RAG] RAG complete. Returning structured results.")
        return results

    except Exception as e:
        print(f"[Tool: PDF_RAG] ERROR: {e}")
        return [{
            "title": "PDF Snippet",
            "url": url,
            "content": f"Error during PDF RAG processing: {str(e)}",
            "source": "pdf_rag",
            "images": []
        }]
