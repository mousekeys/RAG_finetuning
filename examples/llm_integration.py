#!/usr/bin/env python3
"""
Example: Integrating RAG system with a local LLM.

This script demonstrates how to use the RAG system to provide context
to a local LLM for answering questions about financial documents.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem, RAGConfig


def create_prompt(question: str, context: str) -> str:
    """
    Create a prompt for the LLM using the RAG context.
    
    Args:
        question: User's question
        context: Retrieved context from RAG system
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are a helpful financial assistant. Use the following context to answer the question. 
If you cannot answer based on the context, say so.

Context:
{context}

Question: {question}

Answer:"""
    
    return prompt


def main():
    """Main demonstration function."""
    
    print("=" * 70)
    print("RAG System Integration with Local LLM - Example")
    print("=" * 70)
    print()
    
    # Initialize RAG system
    print("Step 1: Initializing RAG system...")
    config = RAGConfig()
    rag = RAGSystem(config)
    print("✓ RAG system initialized\n")
    
    # Load documents
    print("Step 2: Loading documents...")
    data_dir = Path("data")
    if data_dir.exists() and any(data_dir.iterdir()):
        num_docs = rag.load_documents(str(data_dir))
        print(f"✓ Loaded {num_docs} document chunks\n")
    else:
        print("✗ No documents found. Add documents to the 'data' directory first.\n")
        return
    
    # Example questions
    questions = [
        "What is gross profit margin and how is it calculated?",
        "What are the main components of the balance sheet?",
        "Explain the difference between operating cash flow and free cash flow.",
        "What is the current ratio used for?",
    ]
    
    print("Step 3: Processing questions with RAG...\n")
    
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question}")
        print("-" * 70)
        
        # Retrieve relevant context
        result = rag.query(question, top_k=3, return_sources=True)
        
        # Create prompt for LLM
        prompt = create_prompt(question, result['context'])
        
        # Display the prompt (this is what would be sent to your local LLM)
        print("\nPrompt for LLM:")
        print("─" * 70)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        print("─" * 70)
        
        # Display sources
        print(f"\nRetrieved {len(result['sources'])} relevant documents:")
        for j, source in enumerate(result['sources'], 1):
            print(f"\n  Source {j}:")
            print(f"  • File: {source['metadata'].get('source', 'unknown')}")
            print(f"  • Relevance: {source['relevance_score']:.4f}")
            print(f"  • Preview: {source['content'][:100]}...")
        
        print("\n" + "=" * 70 + "\n")
    
    # Instructions for LLM integration
    print("\n" + "=" * 70)
    print("INTEGRATION INSTRUCTIONS")
    print("=" * 70)
    print("""
To integrate with a local LLM:

1. Using llama-cpp-python:
   ```python
   from llama_cpp import Llama
   
   llm = Llama(model_path="path/to/your/model.gguf")
   response = llm(prompt, max_tokens=512, temperature=0.7)
   print(response['choices'][0]['text'])
   ```

2. Using GPT4All:
   ```python
   from gpt4all import GPT4All
   
   model = GPT4All("model_name")
   response = model.generate(prompt, max_tokens=512)
   print(response)
   ```

3. Using Ollama:
   ```python
   import ollama
   
   response = ollama.generate(model='llama2', prompt=prompt)
   print(response['response'])
   ```

The RAG system provides the context, and your local LLM generates
the answer based on that context.
    """)
    print("=" * 70)


if __name__ == "__main__":
    main()
