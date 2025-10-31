"""
RAG Finance Tracking Backend
This module provides a REST API for querying financial documents using RAG with a local LLM.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import chromadb
from sentence_transformers import SentenceTransformer
import os
from datetime import datetime

app = FastAPI(
    title="RAG Finance Tracking API",
    description="API for querying financial documents using Retrieval-Augmented Generation",
    version="1.0.0"
)

# Configure CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Android app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB client (using PersistentClient for the new API)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Initialize embedding model - will download on first run if not cached
# Note: Requires internet connection on first run to download the model
embedding_model = None
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Warning: Could not load embedding model: {e}")
    print("The API will still run but embeddings will not work.")
    print("Make sure you have internet connection on first run to download the model.")

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name="finance_documents",
    metadata={"description": "Financial documents and transactions"}
)


class DocumentInput(BaseModel):
    """Model for adding new financial documents"""
    text: str
    category: str
    amount: Optional[float] = None
    date: Optional[str] = None
    metadata: Optional[dict] = {}


class QueryInput(BaseModel):
    """Model for querying the RAG system"""
    query: str
    n_results: Optional[int] = 5


class QueryResponse(BaseModel):
    """Model for query response"""
    answer: str
    relevant_documents: List[dict]
    timestamp: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RAG Finance Tracking API",
        "status": "active",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/documents/add")
async def add_document(doc: DocumentInput):
    """
    Add a financial document to the vector database
    """
    try:
        if embedding_model is None:
            raise HTTPException(status_code=503, detail="Embedding model not available. Please ensure internet connection on first run to download the model.")
        
        # Generate embedding
        embedding = embedding_model.encode(doc.text).tolist()
        
        # Create metadata
        metadata = doc.metadata or {}
        metadata.update({
            "category": doc.category,
            "amount": doc.amount,
            "date": doc.date or datetime.now().isoformat(),
        })
        
        # Generate unique ID
        doc_id = f"doc_{datetime.now().timestamp()}"
        
        # Add to collection
        collection.add(
            embeddings=[embedding],
            documents=[doc.text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        return {
            "status": "success",
            "message": "Document added successfully",
            "id": doc_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_documents(query: QueryInput):
    """
    Query financial documents using RAG
    This is a simplified version that uses semantic search.
    In a full implementation, this would call a local LLM (like Ollama) to generate responses.
    """
    try:
        if embedding_model is None:
            raise HTTPException(status_code=503, detail="Embedding model not available. Please ensure internet connection on first run to download the model.")
        
        # Generate query embedding
        query_embedding = embedding_model.encode(query.query).tolist()
        
        # Search in vector database
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=query.n_results
        )
        
        # Format relevant documents
        relevant_docs = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                relevant_docs.append({
                    "text": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else None
                })
        
        # Generate answer (simplified - in production, use local LLM)
        if relevant_docs:
            answer = self._generate_answer(query.query, relevant_docs)
        else:
            answer = "No relevant financial documents found for your query."
        
        return QueryResponse(
            answer=answer,
            relevant_documents=relevant_docs,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _generate_answer(query: str, relevant_docs: List[dict]) -> str:
    """
    Generate answer from relevant documents
    This is a simplified version. In production, integrate with Ollama or similar local LLM.
    """
    # Extract information from relevant documents
    context = "\n".join([doc["text"] for doc in relevant_docs[:3]])
    
    # Simple template-based response
    answer = f"Based on your financial records:\n\n{context}\n\n"
    answer += "Note: This is a basic RAG system. For more sophisticated responses, "
    answer += "integrate with a local LLM like Ollama running Llama 2 or similar models."
    
    return answer


@app.get("/documents/count")
async def get_document_count():
    """Get the total count of documents in the database"""
    try:
        count = collection.count()
        return {
            "count": count,
            "collection": "finance_documents"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents/clear")
async def clear_documents():
    """Clear all documents from the database (use with caution)"""
    try:
        global collection
        chroma_client.delete_collection("finance_documents")
        collection = chroma_client.get_or_create_collection(
            name="finance_documents",
            metadata={"description": "Financial documents and transactions"}
        )
        return {
            "status": "success",
            "message": "All documents cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
