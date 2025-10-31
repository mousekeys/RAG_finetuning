#!/usr/bin/env python3
"""
Command-line interface for RAG Finance Tracking System.

This provides a simple CLI for interacting with the RAG system.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem, RAGConfig


def load_documents(rag: RAGSystem, path: str) -> None:
    """Load documents into the RAG system."""
    print(f"Loading documents from: {path}")
    try:
        num_docs = rag.load_documents(path)
        print(f"Successfully loaded {num_docs} document chunks")
    except Exception as e:
        print(f"Error loading documents: {e}")
        sys.exit(1)


def query_documents(rag: RAGSystem, question: str, top_k: int) -> None:
    """Query the RAG system."""
    print(f"\nQuestion: {question}\n")
    
    result = rag.query(question, top_k=top_k, return_sources=True)
    
    print("Context:")
    print("-" * 70)
    print(result['context'])
    print("-" * 70)
    
    if result['sources']:
        print(f"\nSources ({len(result['sources'])} documents):")
        for i, source in enumerate(result['sources'], 1):
            print(f"\n{i}. File: {source['metadata'].get('source', 'unknown')}")
            print(f"   Relevance: {source['relevance_score']:.4f}")
            if 'page' in source['metadata']:
                print(f"   Page: {source['metadata']['page']}")


def show_stats(rag: RAGSystem) -> None:
    """Display RAG system statistics."""
    stats = rag.get_stats()
    
    print("\nRAG System Statistics:")
    print("=" * 50)
    for key, value in stats.items():
        print(f"{key:20s}: {value}")
    print("=" * 50)


def clear_database(rag: RAGSystem) -> None:
    """Clear the vector database."""
    confirm = input("Are you sure you want to clear the database? (yes/no): ")
    if confirm.lower() == 'yes':
        rag.clear_database()
        print("Database cleared successfully")
    else:
        print("Operation cancelled")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="RAG Finance Tracking System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load documents
  %(prog)s load data/
  
  # Query the system
  %(prog)s query "What is revenue?"
  
  # Show statistics
  %(prog)s stats
  
  # Clear database
  %(prog)s clear
        """
    )
    
    parser.add_argument(
        'command',
        choices=['load', 'query', 'stats', 'clear'],
        help='Command to execute'
    )
    
    parser.add_argument(
        'argument',
        nargs='?',
        help='Argument for the command (path for load, question for query)'
    )
    
    parser.add_argument(
        '--top-k',
        type=int,
        default=4,
        help='Number of documents to retrieve (default: 4)'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=1000,
        help='Chunk size for document processing (default: 1000)'
    )
    
    parser.add_argument(
        '--chunk-overlap',
        type=int,
        default=200,
        help='Chunk overlap (default: 200)'
    )
    
    args = parser.parse_args()
    
    # Initialize RAG system
    print("Initializing RAG system...")
    config = RAGConfig(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        top_k=args.top_k
    )
    rag = RAGSystem(config)
    print("RAG system initialized\n")
    
    # Execute command
    if args.command == 'load':
        if not args.argument:
            print("Error: path argument required for load command")
            sys.exit(1)
        load_documents(rag, args.argument)
    
    elif args.command == 'query':
        if not args.argument:
            print("Error: question argument required for query command")
            sys.exit(1)
        query_documents(rag, args.argument, args.top_k)
    
    elif args.command == 'stats':
        show_stats(rag)
    
    elif args.command == 'clear':
        clear_database(rag)


if __name__ == "__main__":
    main()
