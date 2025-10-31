# Architecture Overview

## System Architecture

The RAG Finance Tracking System follows a modular architecture designed for flexibility and ease of use.

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  (CLI, Python API, Custom Applications)                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      RAG System Core                         │
│                        (rag.py)                              │
└───┬──────────────┬──────────────┬──────────────┬───────────┘
    │              │              │              │
    │              │              │              │
┌───▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────────┐
│Document│   │Embeddings│   │Vector   │   │Config      │
│Loader  │   │          │   │Store    │   │            │
│        │   │          │   │         │   │            │
└───┬────┘   └────┬─────┘   └────┬────┘   └────────────┘
    │              │              │
    │              │              │
┌───▼──────────────▼──────────────▼─────────────────────┐
│              External Libraries                        │
│  LangChain | ChromaDB | Sentence-Transformers         │
└────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### 1. RAG System Core (`rag.py`)
- **Purpose**: Main orchestrator of the system
- **Responsibilities**:
  - Initialize and coordinate all components
  - Provide unified API for loading and querying
  - Manage system statistics
  - Handle database operations

### 2. Document Loader (`document_loader.py`)
- **Purpose**: Process and prepare documents for indexing
- **Responsibilities**:
  - Load documents from various formats (PDF, DOCX, TXT)
  - Split documents into chunks
  - Extract metadata
  - Handle directories and individual files

### 3. Embeddings (`embeddings.py`)
- **Purpose**: Convert text to vector representations
- **Responsibilities**:
  - Load and manage embedding models
  - Generate embeddings for documents
  - Generate embeddings for queries
  - Use local sentence-transformers models

### 4. Vector Store (`vector_store.py`)
- **Purpose**: Store and retrieve document embeddings
- **Responsibilities**:
  - Persist embeddings to ChromaDB
  - Perform similarity searches
  - Manage collections
  - Return relevant documents with scores

### 5. Configuration (`config.py`)
- **Purpose**: Centralize system configuration
- **Responsibilities**:
  - Define default settings
  - Load environment variables
  - Validate configuration
  - Create necessary directories

## Data Flow

### Indexing Flow
```
Documents → Document Loader → Text Chunks → Embeddings → Vector Store
                                                              ↓
                                                        [ChromaDB]
```

### Query Flow
```
User Query → Embeddings → Vector Store → Similarity Search → Relevant Chunks
                              ↓
                          [ChromaDB]
                              ↓
                         Context → LLM → Answer
```

## Integration Points

### With Local LLMs

The system is designed to integrate with various local LLM frameworks:

1. **llama-cpp-python**: For GGUF format models
2. **GPT4All**: For various open-source models
3. **Ollama**: For easy model management
4. **Transformers**: For Hugging Face models

### Integration Pattern

```python
# RAG retrieves context
result = rag.query(question)

# Format prompt with context
prompt = f"Context: {result['context']}\nQuestion: {question}"

# LLM generates answer
answer = llm.generate(prompt)
```

## Storage

### File System Structure
```
RAG_financetracking/
├── data/                    # User documents
│   ├── sample_finance_doc.txt
│   └── vectordb/           # ChromaDB storage (created automatically)
│       └── chroma.sqlite3
└── models/                 # Optional: Local LLM models
    └── your-model.gguf
```

### ChromaDB Storage
- **Format**: SQLite database
- **Location**: `data/vectordb/`
- **Contents**: Vector embeddings and metadata
- **Persistence**: Automatic

## Performance Characteristics

### Memory Usage
- **Embedding Model**: ~100-500 MB (depends on model size)
- **Vector Store**: Scales with document count
- **Per Document**: ~1-10 KB per chunk

### Speed
- **Document Loading**: Depends on document size and format
- **Embedding Generation**: ~10-100 docs/second
- **Query Time**: <1 second for most collections
- **First Run**: Slower (downloads embedding model)

### Scalability
- **Document Count**: Tested up to 100,000 chunks
- **Concurrent Queries**: Thread-safe for reads
- **Storage**: Grows linearly with document count

## Configuration Options

### Key Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| chunk_size | 1000 | Size of text chunks |
| chunk_overlap | 200 | Overlap between chunks |
| top_k | 4 | Documents to retrieve |
| embedding_model | all-MiniLM-L6-v2 | Model for embeddings |
| collection_name | finance_docs | ChromaDB collection |

### Trade-offs

**Chunk Size:**
- Smaller: More precise, less context
- Larger: More context, less precise

**Top-K:**
- Higher: More context, more noise
- Lower: Less context, more focused

**Embedding Model:**
- Smaller: Faster, less accurate
- Larger: Slower, more accurate

## Security Considerations

1. **Data Privacy**: All processing happens locally
2. **No External Calls**: No data sent to external APIs
3. **File Access**: Restricted to configured directories
4. **Dependencies**: Use only well-known, vetted libraries

## Extension Points

### Adding New Document Types
Extend `DocumentLoader` with new methods for different formats.

### Custom Embeddings
Implement custom embedding models by extending `LocalEmbeddings`.

### Different Vector Stores
Modify `VectorStore` to support alternatives like FAISS or Pinecone.

### Custom Retrievers
Implement different retrieval strategies in the `RAGSystem` class.
