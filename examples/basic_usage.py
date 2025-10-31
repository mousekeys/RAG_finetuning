#!/usr/bin/env python3
"""
Example script demonstrating the RAG Finance Tracking System.

This script shows how to:
1. Initialize the RAG system
2. Load documents
3. Query the system
4. View statistics
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem, RAGConfig


def main():
    """Main example function."""
    
    print("=" * 60)
    print("RAG Finance Tracking System - Example Usage")
    print("=" * 60)
    print()
    
    # Initialize the RAG system
    print("1. Initializing RAG system...")
    config = RAGConfig()
    rag = RAGSystem(config)
    print()
    
    # Display current statistics
    print("2. Current system statistics:")
    stats = rag.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    # Example: Load documents (if data directory has files)
    data_dir = Path("data")
    if data_dir.exists() and any(data_dir.iterdir()):
        print("3. Loading documents from data directory...")
        try:
            num_docs = rag.load_documents(str(data_dir))
            print(f"   Loaded {num_docs} document chunks")
        except Exception as e:
            print(f"   Error loading documents: {e}")
    else:
        print("3. No documents found in data directory.")
        print("   To use this system, add documents to the 'data' directory.")
        print("   Supported formats: .txt, .pdf, .docx")
    print()
    
    # Example query
    print("4. Example query:")
    query = "What are the main financial concepts?"
    print(f"   Question: {query}")
    result = rag.query(query, top_k=3)
    
    if result['sources']:
        print(f"\n   Found {len(result['sources'])} relevant documents:")
        for i, source in enumerate(result['sources'], 1):
            print(f"\n   Source {i}:")
            print(f"   - Relevance score: {source['relevance_score']:.4f}")
            print(f"   - Metadata: {source['metadata']}")
            print(f"   - Content preview: {source['content'][:150]}...")
    else:
        print("   No relevant documents found.")
    print()
    
    # Display updated statistics
    print("5. Updated system statistics:")
    stats = rag.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    print("=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
