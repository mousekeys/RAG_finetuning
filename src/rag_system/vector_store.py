"""
Vector store module for RAG Finance Tracking System.

This module handles vector database operations using ChromaDB for local storage.
"""

from pathlib import Path
from typing import List, Optional
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings


class VectorStore:
    """Handles vector database operations using ChromaDB."""
    
    def __init__(
        self,
        embeddings: Embeddings,
        persist_directory: str = "data/vectordb",
        collection_name: str = "finance_docs"
    ):
        """
        Initialize the vector store.
        
        Args:
            embeddings: Embeddings model to use
            persist_directory: Directory to persist the vector database
            collection_name: Name of the ChromaDB collection
        """
        self.embeddings = embeddings
        self.persist_directory = str(persist_directory)
        self.collection_name = collection_name
        
        # Ensure persist directory exists
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize or load the vector store
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=self.persist_directory
        )
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            print("No documents to add.")
            return
        
        self.vectorstore.add_documents(documents)
        print(f"Added {len(documents)} documents to the vector store.")
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter_dict: Optional[dict] = None
    ) -> List[Document]:
        """
        Search for similar documents.
        
        Args:
            query: Query text
            k: Number of documents to return
            filter_dict: Optional metadata filter
            
        Returns:
            List of similar documents
        """
        results = self.vectorstore.similarity_search(
            query,
            k=k,
            filter=filter_dict
        )
        return results
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter_dict: Optional[dict] = None
    ) -> List[tuple]:
        """
        Search for similar documents with relevance scores.
        
        Args:
            query: Query text
            k: Number of documents to return
            filter_dict: Optional metadata filter
            
        Returns:
            List of tuples (document, score)
        """
        results = self.vectorstore.similarity_search_with_score(
            query,
            k=k,
            filter=filter_dict
        )
        return results
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        self.vectorstore.delete_collection()
        print(f"Deleted collection: {self.collection_name}")
    
    def get_document_count(self) -> int:
        """
        Get the number of documents in the vector store.
        
        Returns:
            Number of documents
        """
        try:
            collection = self.vectorstore._collection
            return collection.count()
        except Exception as e:
            print(f"Error getting document count: {e}")
            return 0
