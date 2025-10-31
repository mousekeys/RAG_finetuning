"""
Configuration module for RAG Finance Tracking System.

This module handles configuration settings for the RAG system including
paths, model settings, and vector store parameters.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class RAGConfig(BaseModel):
    """Configuration for RAG system."""
    
    # Paths
    data_dir: Path = Field(default=Path("data"), description="Directory for storing documents")
    vector_db_dir: Path = Field(default=Path("data/vectordb"), description="Directory for vector database")
    models_dir: Path = Field(default=Path("models"), description="Directory for local models")
    
    # Embedding settings
    embedding_model_name: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Name of the embedding model"
    )
    
    # Vector store settings
    collection_name: str = Field(default="finance_docs", description="ChromaDB collection name")
    chunk_size: int = Field(default=1000, description="Size of text chunks for processing")
    chunk_overlap: int = Field(default=200, description="Overlap between chunks")
    
    # Retrieval settings
    top_k: int = Field(default=4, description="Number of documents to retrieve")
    
    # LLM settings
    llm_model_path: Optional[str] = Field(default=None, description="Path to local LLM model")
    llm_temperature: float = Field(default=0.7, description="Temperature for LLM generation")
    llm_max_tokens: int = Field(default=512, description="Maximum tokens for LLM response")
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.vector_db_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)


def load_config() -> RAGConfig:
    """
    Load configuration from environment variables or use defaults.
    
    Returns:
        RAGConfig: Configuration object
    """
    config = RAGConfig()
    config.ensure_directories()
    return config
