# Create this file: insightbridge/mcp/adapters/pdf_rag_adapter.py

import os
import requests
import pymupdf  # PDF text extraction
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# Initialize components once for efficiency
print("[Tool: PDF_RAG] Initializing components (Embeddings, Splitter)...")
embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
print("[Tool: PDF_RAG] Components ready.")

def pdf_rag_query(url: str, query: str) -> str:
    """
    Performs a full RAG workflow on a live PDF URL.
    This function expects to be called with keyword arguments.
    """
    print(f"\n[Tool: PDF_RAG] Starting RAG for URL: {url}")
    try:
        # 1. Download the PDF
        print(f"[Tool: PDF_RAG] Downloading PDF...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 2. Extract Text (in-memory)
        print("[Tool: PDF_RAG] Extracting text from PDF...")
        with pymupdf.open("pdf", response.content) as doc:
            full_text = "".join(page.get_text() for page in doc)
            
        if not full_text:
            return "Error: Could not extract any text from the PDF."

        # 3. Chunk the Text
        print(f"[Tool: PDF_RAG] Splitting {len(full_text)} chars into chunks...")
        chunks = text_splitter.split_text(full_text)
        
        # 4. Embed and Store (In-Memory Vector Store)
        print(f"[Tool: PDF_RAG] Creating in-memory vector store with {len(chunks)} chunks...")
        vector_store = Chroma.from_texts(
            texts=chunks, 
            embedding=embeddings_model
        )
        
        # 5. Retrieve Relevant Chunks
        print(f"[Tool: PDF_RAG] Searching for relevant chunks: {query}")
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(query)
        
        # 6. Format and Return
        # We just return the snippets. The /deep-dive endpoint
        # will pass these to an LLM to generate a final answer.
        context_snippets = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])
        print("[Tool: PDF_RAG] RAG complete. Returning snippets.")
        return context_snippets
        
    except Exception as e:
        print(f"[Tool: PDF_RAG] ERROR: {e}")
        return f"Error during RAG process for {url}: {e}"