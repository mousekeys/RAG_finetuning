"""
Main RAG system module for Finance Tracking.

This module integrates all components to provide a complete RAG system
that works with local LLMs.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
from langchain.schema import Document

from .config import RAGConfig, load_config
from .document_loader import DocumentLoader
from .embeddings import LocalEmbeddings
from .vector_store import VectorStore


class RAGSystem:
    """Main RAG system class that integrates all components."""
    
    def __init__(self, config: Optional[RAGConfig] = None):
        """
        Initialize the RAG system.
        
        Args:
            config: Optional configuration object. If not provided, defaults will be used.
        """
        self.config = config or load_config()
        
        # Initialize embeddings
        print(f"Loading embeddings model: {self.config.embedding_model_name}")
        self.embeddings = LocalEmbeddings(model_name=self.config.embedding_model_name)
        
        # Initialize vector store
        print(f"Initializing vector store at: {self.config.vector_db_dir}")
        self.vector_store = VectorStore(
            embeddings=self.embeddings,
            persist_directory=str(self.config.vector_db_dir),
            collection_name=self.config.collection_name
        )
        
        # Initialize document loader
        self.document_loader = DocumentLoader(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap
        )
        
        print("RAG system initialized successfully.")
    
    def load_documents(self, path: str) -> int:
        """
        Load documents from a file or directory.
        
        Args:
            path: Path to file or directory
            
        Returns:
            Number of document chunks loaded
        """
        path_obj = Path(path)
        
        if not path_obj.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        if path_obj.is_file():
            documents = self.document_loader.load_document(path_obj)
        else:
            documents = self.document_loader.load_directory(path_obj)
        
        if documents:
            self.vector_store.add_documents(documents)
            print(f"Successfully loaded {len(documents)} document chunks.")
        else:
            print("No documents were loaded.")
        
        return len(documents)
    
    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        return_sources: bool = True
    ) -> Dict[str, Any]:
        """
        Query the RAG system.
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve (uses config default if not provided)
            return_sources: Whether to return source documents
            
        Returns:
            Dictionary containing the context and optionally source documents
        """
        k = top_k or self.config.top_k
        
        # Retrieve relevant documents
        results = self.vector_store.similarity_search_with_score(question, k=k)
        
        if not results:
            return {
                "context": "No relevant documents found.",
                "sources": [] if return_sources else None
            }
        
        # Build context from retrieved documents
        context_parts = []
        sources = []
        
        for i, (doc, score) in enumerate(results, 1):
            context_parts.append(f"Document {i}:\n{doc.page_content}")
            if return_sources:
                sources.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": float(score)
                })
        
        context = "\n\n".join(context_parts)
        
        result = {
            "question": question,
            "context": context,
        }
        
        if return_sources:
            result["sources"] = sources
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG system.
        
        Returns:
            Dictionary containing system statistics
        """
        doc_count = self.vector_store.get_document_count()
        
        return {
            "document_count": doc_count,
            "collection_name": self.config.collection_name,
            "embedding_model": self.config.embedding_model_name,
            "chunk_size": self.config.chunk_size,
            "chunk_overlap": self.config.chunk_overlap,
        }
    
    def clear_database(self) -> None:
        """Clear all documents from the vector database."""
        self.vector_store.delete_collection()
        # Reinitialize the vector store
        self.vector_store = VectorStore(
            embeddings=self.embeddings,
            persist_directory=str(self.config.vector_db_dir),
            collection_name=self.config.collection_name
        )
        print("Database cleared successfully.")
