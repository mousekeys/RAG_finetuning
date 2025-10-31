# API Reference

Complete API documentation for the RAG Finance Tracking System.

## Core Classes

### RAGSystem

The main class for interacting with the RAG system.

```python
from src.rag_system import RAGSystem, RAGConfig

# Initialize with default configuration
rag = RAGSystem()

# Initialize with custom configuration
config = RAGConfig(chunk_size=500, top_k=5)
rag = RAGSystem(config)
```

#### Methods

##### `__init__(config: Optional[RAGConfig] = None)`

Initialize the RAG system.

**Parameters:**
- `config` (RAGConfig, optional): Configuration object. Uses defaults if not provided.

**Example:**
```python
rag = RAGSystem()
```

---

##### `load_documents(path: str) -> int`

Load documents from a file or directory.

**Parameters:**
- `path` (str): Path to file or directory

**Returns:**
- `int`: Number of document chunks loaded

**Raises:**
- `FileNotFoundError`: If path doesn't exist
- `ValueError`: If file type is not supported

**Example:**
```python
# Load from directory
num_docs = rag.load_documents("data/")

# Load single file
num_docs = rag.load_documents("data/report.pdf")
```

---

##### `query(question: str, top_k: Optional[int] = None, return_sources: bool = True) -> Dict[str, Any]`

Query the RAG system to retrieve relevant context.

**Parameters:**
- `question` (str): User's question
- `top_k` (int, optional): Number of documents to retrieve. Uses config default if not provided.
- `return_sources` (bool): Whether to return source documents. Default: True

**Returns:**
- `dict`: Dictionary containing:
  - `question` (str): The original question
  - `context` (str): Retrieved context from documents
  - `sources` (list, optional): List of source documents with metadata and scores

**Example:**
```python
result = rag.query("What is revenue?", top_k=3)

print(result['question'])   # Original question
print(result['context'])    # Retrieved context
print(result['sources'])    # Source documents
```

---

##### `get_stats() -> Dict[str, Any]`

Get statistics about the RAG system.

**Returns:**
- `dict`: Dictionary containing system statistics

**Example:**
```python
stats = rag.get_stats()
print(f"Documents: {stats['document_count']}")
print(f"Model: {stats['embedding_model']}")
```

---

##### `clear_database() -> None`

Clear all documents from the vector database.

**Warning:** This operation cannot be undone.

**Example:**
```python
rag.clear_database()
```

---

### RAGConfig

Configuration class for the RAG system.

```python
from src.rag_system import RAGConfig

config = RAGConfig(
    chunk_size=1000,
    chunk_overlap=200,
    top_k=4,
    embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| data_dir | Path | "data" | Directory for documents |
| vector_db_dir | Path | "data/vectordb" | Directory for vector database |
| models_dir | Path | "models" | Directory for models |
| embedding_model_name | str | "sentence-transformers/all-MiniLM-L6-v2" | Embedding model |
| collection_name | str | "finance_docs" | ChromaDB collection name |
| chunk_size | int | 1000 | Text chunk size |
| chunk_overlap | int | 200 | Chunk overlap |
| top_k | int | 4 | Documents to retrieve |
| llm_model_path | str | None | Path to local LLM |
| llm_temperature | float | 0.7 | LLM temperature |
| llm_max_tokens | int | 512 | Max LLM tokens |

#### Methods

##### `ensure_directories()`

Create necessary directories if they don't exist.

---

### DocumentLoader

Handles loading and processing of documents.

```python
from src.rag_system import DocumentLoader

loader = DocumentLoader(chunk_size=1000, chunk_overlap=200)
```

#### Methods

##### `load_text_file(file_path: Union[str, Path]) -> List[Document]`

Load a text file.

**Parameters:**
- `file_path`: Path to the text file

**Returns:**
- `List[Document]`: List of document chunks

---

##### `load_pdf_file(file_path: Union[str, Path]) -> List[Document]`

Load a PDF file.

**Parameters:**
- `file_path`: Path to the PDF file

**Returns:**
- `List[Document]`: List of document chunks

**Requires:** pypdf library

---

##### `load_docx_file(file_path: Union[str, Path]) -> List[Document]`

Load a DOCX file.

**Parameters:**
- `file_path`: Path to the DOCX file

**Returns:**
- `List[Document]`: List of document chunks

**Requires:** python-docx library

---

##### `load_directory(directory_path: Union[str, Path]) -> List[Document]`

Load all supported documents from a directory.

**Parameters:**
- `directory_path`: Path to the directory

**Returns:**
- `List[Document]`: List of document chunks from all files

---

##### `load_document(file_path: Union[str, Path]) -> List[Document]`

Load a single document, auto-detecting the file type.

**Parameters:**
- `file_path`: Path to the document

**Returns:**
- `List[Document]`: List of document chunks

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If file type is unsupported

---

### LocalEmbeddings

Local embeddings using sentence-transformers.

```python
from src.rag_system import LocalEmbeddings

embeddings = LocalEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
```

#### Methods

##### `embed_documents(texts: List[str]) -> List[List[float]]`

Embed a list of documents.

**Parameters:**
- `texts`: List of text strings

**Returns:**
- `List[List[float]]`: List of embedding vectors

---

##### `embed_query(text: str) -> List[float]`

Embed a single query.

**Parameters:**
- `text`: Query text

**Returns:**
- `List[float]`: Embedding vector

---

### VectorStore

Handles vector database operations using ChromaDB.

```python
from src.rag_system import VectorStore, LocalEmbeddings

embeddings = LocalEmbeddings()
vector_store = VectorStore(
    embeddings=embeddings,
    persist_directory="data/vectordb",
    collection_name="finance_docs"
)
```

#### Methods

##### `add_documents(documents: List[Document]) -> None`

Add documents to the vector store.

**Parameters:**
- `documents`: List of Document objects

---

##### `similarity_search(query: str, k: int = 4, filter_dict: Optional[dict] = None) -> List[Document]`

Search for similar documents.

**Parameters:**
- `query`: Query text
- `k`: Number of documents to return
- `filter_dict`: Optional metadata filter

**Returns:**
- `List[Document]`: List of similar documents

---

##### `similarity_search_with_score(query: str, k: int = 4, filter_dict: Optional[dict] = None) -> List[tuple]`

Search for similar documents with relevance scores.

**Parameters:**
- `query`: Query text
- `k`: Number of documents to return
- `filter_dict`: Optional metadata filter

**Returns:**
- `List[tuple]`: List of (document, score) tuples

---

##### `get_document_count() -> int`

Get the number of documents in the vector store.

**Returns:**
- `int`: Number of documents

---

## Usage Examples

### Basic Usage

```python
from src.rag_system import RAGSystem

# Initialize
rag = RAGSystem()

# Load documents
rag.load_documents("data/")

# Query
result = rag.query("What is revenue?")
print(result['context'])
```

### Custom Configuration

```python
from src.rag_system import RAGSystem, RAGConfig

# Create custom config
config = RAGConfig(
    chunk_size=500,
    chunk_overlap=100,
    top_k=5,
    embedding_model_name="sentence-transformers/all-mpnet-base-v2"
)

# Initialize with config
rag = RAGSystem(config)
```

### Advanced Querying

```python
# Query with custom top_k
result = rag.query("What is cash flow?", top_k=3)

# Access sources
for i, source in enumerate(result['sources'], 1):
    print(f"Source {i}:")
    print(f"  File: {source['metadata']['source']}")
    print(f"  Score: {source['relevance_score']:.4f}")
    print(f"  Content: {source['content'][:100]}...")
```

### Working with Specific Files

```python
from src.rag_system import DocumentLoader

loader = DocumentLoader()

# Load specific file
docs = loader.load_document("data/report.pdf")
print(f"Loaded {len(docs)} chunks from PDF")

# Load text file
docs = loader.load_text_file("data/notes.txt")
```

### Custom Embeddings

```python
from src.rag_system import LocalEmbeddings

# Use different embedding model
embeddings = LocalEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Embed query
query_embedding = embeddings.embed_query("What is profit?")
print(f"Embedding dimension: {len(query_embedding)}")
```

## Error Handling

```python
try:
    rag = RAGSystem()
    rag.load_documents("data/")
    result = rag.query("question")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid value: {e}")
except ImportError as e:
    print(f"Missing dependency: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Type Hints

The library uses type hints throughout. For best IDE support:

```python
from typing import List, Dict, Any, Optional
from pathlib import Path
from langchain.schema import Document
from src.rag_system import RAGSystem, RAGConfig

def process_documents(path: str) -> Dict[str, Any]:
    rag: RAGSystem = RAGSystem()
    count: int = rag.load_documents(path)
    result: Dict[str, Any] = rag.query("question")
    return result
```
