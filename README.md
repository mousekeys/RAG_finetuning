# RAG Finance Tracking System

A Retrieval-Augmented Generation (RAG) system designed for financial document processing and question-answering using local Large Language Models (LLMs).

## Overview

This system provides a base implementation for building RAG applications that work with financial documents. It includes:

- **Document Loading**: Support for multiple document formats (PDF, DOCX, TXT)
- **Text Chunking**: Intelligent text splitting with configurable chunk sizes and overlap
- **Vector Storage**: Local vector database using ChromaDB for document embeddings
- **Embeddings**: Local embedding models using sentence-transformers
- **Retrieval**: Semantic search to find relevant document chunks
- **Local LLM Support**: Designed to work with local LLMs (e.g., via llama-cpp-python)

## Features

- 🔒 **Privacy-First**: All processing happens locally - no data sent to external APIs
- 📚 **Multi-Format Support**: Process PDF, DOCX, and TXT files
- 🎯 **Semantic Search**: Find relevant information using vector similarity
- ⚙️ **Configurable**: Easy-to-configure settings for chunks, embeddings, and retrieval
- 🚀 **Easy to Use**: Simple API for loading documents and querying

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/mousekeys/RAG_financetracking.git
cd RAG_financetracking
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from src.rag_system import RAGSystem

# Initialize the RAG system
rag = RAGSystem()

# Load documents from a directory
rag.load_documents("data/")

# Query the system
result = rag.query("What are the key financial metrics?")

# Access the retrieved context
print(result['context'])

# View source documents
for source in result['sources']:
    print(f"Source: {source['metadata']}")
    print(f"Relevance: {source['relevance_score']}")
```

### Running the Example

```bash
python examples/basic_usage.py
```

## Project Structure

```
RAG_financetracking/
├── src/
│   └── rag_system/
│       ├── __init__.py          # Package initialization
│       ├── config.py             # Configuration management
│       ├── document_loader.py    # Document loading and processing
│       ├── embeddings.py         # Embedding model wrapper
│       ├── vector_store.py       # Vector database operations
│       └── rag.py                # Main RAG system
├── examples/
│   └── basic_usage.py            # Example usage script
├── data/                         # Place your documents here
├── tests/                        # Test files
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Configuration

The system can be configured through the `RAGConfig` class:

```python
from src.rag_system import RAGConfig, RAGSystem

config = RAGConfig(
    chunk_size=1000,              # Size of text chunks
    chunk_overlap=200,            # Overlap between chunks
    top_k=4,                      # Number of documents to retrieve
    embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"
)

rag = RAGSystem(config)
```

## Supported Document Formats

- **PDF** (.pdf): Extracted using pypdf
- **Word Documents** (.docx): Extracted using python-docx
- **Text Files** (.txt): Direct text reading

## Components

### Document Loader
Handles loading and chunking of documents from various formats.

### Embeddings
Uses sentence-transformers to create vector embeddings of text chunks locally.

### Vector Store
Stores and retrieves document embeddings using ChromaDB, a local vector database.

### RAG System
Main orchestrator that combines all components to provide a simple API.

## Working with Local LLMs

This system is designed to work with local LLMs. The retrieval system provides relevant context that can be fed to any local LLM. Example integration:

```python
from src.rag_system import RAGSystem

# Initialize RAG system
rag = RAGSystem()

# Get relevant context for a question
result = rag.query("What is the company's revenue?")

# Use the context with your local LLM
prompt = f"""
Based on the following context, answer the question.

Context:
{result['context']}

Question: {result['question']}

Answer:
"""

# Feed the prompt to your local LLM (llama-cpp-python, GPT4All, etc.)
# response = your_llm.generate(prompt)
```

## Development

### Adding New Document Types

To add support for new document types, extend the `DocumentLoader` class:

```python
def load_custom_format(self, file_path):
    # Your loading logic here
    pass
```

### Customizing Embeddings

You can use different embedding models by changing the model name:

```python
config = RAGConfig(
    embedding_model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
```

## Use Cases

- **Financial Report Analysis**: Query annual reports, financial statements
- **Document Q&A**: Ask questions about your financial documents
- **Information Retrieval**: Find relevant sections in large document collections
- **Research Assistant**: Quickly locate specific financial information

## Performance Considerations

- **Chunk Size**: Larger chunks provide more context but may reduce precision
- **Overlap**: More overlap improves context continuity but increases storage
- **Embedding Model**: Smaller models are faster but may be less accurate
- **Top-K**: Retrieving more documents provides more context but may include irrelevant information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and research purposes.

## Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Embeddings by [sentence-transformers](https://www.sbert.net/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)