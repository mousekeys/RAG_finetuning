"""
RAG Finance Tracking System

A Retrieval-Augmented Generation system for working with financial documents
and local LLMs.
"""

from .config import RAGConfig, load_config
from .rag import RAGSystem
from .document_loader import DocumentLoader
from .embeddings import LocalEmbeddings
from .vector_store import VectorStore

__all__ = [
    'RAGConfig',
    'load_config',
    'RAGSystem',
    'DocumentLoader',
    'LocalEmbeddings',
    'VectorStore',
]

__version__ = '0.1.0'
