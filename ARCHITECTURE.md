# RAG Finance Tracking - Architecture Documentation

## System Architecture

### Overview

This system implements a Retrieval-Augmented Generation (RAG) architecture for finance tracking, consisting of a Python backend and an Android mobile application.

```
┌─────────────────────────────────────────────────────────────┐
│                     Android Application                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                      UI Layer                          │  │
│  │  - Jetpack Compose                                     │  │
│  │  - Material Design 3                                   │  │
│  │  - Query & Add Document Screens                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                          ↕                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  ViewModel Layer                       │  │
│  │  - State Management                                    │  │
│  │  - Business Logic                                      │  │
│  │  - Coroutines                                          │  │
│  └───────────────────────────────────────────────────────┘  │
│                          ↕                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                Repository Layer                        │  │
│  │  - Data Operations                                     │  │
│  │  - Error Handling                                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                          ↕                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Network Layer                        │  │
│  │  - Retrofit HTTP Client                               │  │
│  │  - API Service Interface                              │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
                         HTTP/REST
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      Backend Server                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    FastAPI                             │  │
│  │  - REST API Endpoints                                  │  │
│  │  - CORS Middleware                                     │  │
│  │  - Request Validation (Pydantic)                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                          ↕                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              RAG Processing Layer                      │  │
│  │  - Query Processing                                    │  │
│  │  - Document Embedding                                  │  │
│  │  - Semantic Search                                     │  │
│  │  - Response Generation                                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                          ↕                                   │
│  ┌─────────────────┐           ┌─────────────────────────┐  │
│  │  Embeddings     │           │   Local LLM (Optional)  │  │
│  │  SentenceTransf.│           │   - Ollama/Llama 2      │  │
│  │  MiniLM-L6-v2   │           │   - Response Generation │  │
│  └─────────────────┘           └─────────────────────────┘  │
│                          ↕                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                Vector Database                         │  │
│  │  - ChromaDB                                            │  │
│  │  - Document Storage                                    │  │
│  │  - Similarity Search                                   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Android Application

#### UI Layer (Jetpack Compose)
- **FinanceScreen.kt**: Main composable screen with tabs
  - Query Tab: Input queries and display results
  - Add Document Tab: Form to add financial documents
- **Theme**: Material Design 3 with custom colors
- **Navigation**: Tab-based navigation

#### ViewModel Layer
- **FinanceViewModel.kt**: Manages UI state and business logic
  - State management using StateFlow
  - Coroutine-based async operations
  - UI state (Idle, Loading, Success, Error)

#### Repository Layer
- **FinanceRepository.kt**: Data operations
  - API calls to backend
  - Error handling
  - Data transformation

#### Network Layer
- **ApiClient.kt**: Retrofit configuration
  - HTTP client setup
  - Logging interceptor
  - Base URL configuration
- **FinanceApiService.kt**: API interface definitions
  - Request/Response models
  - HTTP method definitions

### 2. Backend Server

#### API Layer (FastAPI)
**Endpoints:**
- `GET /`: Root endpoint with API info
- `GET /health`: Health check
- `POST /documents/add`: Add financial document
- `POST /query`: Query documents using RAG
- `GET /documents/count`: Get document count
- `DELETE /documents/clear`: Clear all documents

#### RAG Processing
1. **Document Ingestion**:
   - Text received from API
   - Embedding generated using SentenceTransformers
   - Stored in ChromaDB with metadata (category, amount, date)

2. **Query Processing**:
   - Query text embedded
   - Semantic search in ChromaDB
   - Top N relevant documents retrieved
   - Response generated (basic or LLM-enhanced)

#### Vector Database (ChromaDB)
- **Storage**: Local file-based persistence
- **Collection**: finance_documents
- **Embedding Model**: all-MiniLM-L6-v2
- **Similarity Metric**: Cosine similarity (default)

## Data Flow

### Adding a Document

```
User Input (Android)
    ↓
ViewModel.addDocument()
    ↓
Repository.addDocument()
    ↓
HTTP POST /documents/add
    ↓
FastAPI Endpoint
    ↓
Generate Embedding
    ↓
Store in ChromaDB
    ↓
Response Success
    ↓
Update UI State
```

### Querying Documents

```
User Query (Android)
    ↓
ViewModel.queryDocuments()
    ↓
Repository.queryDocuments()
    ↓
HTTP POST /query
    ↓
FastAPI Endpoint
    ↓
Generate Query Embedding
    ↓
Semantic Search in ChromaDB
    ↓
Retrieve Top N Documents
    ↓
Generate Response (Template/LLM)
    ↓
Return QueryResponse
    ↓
Display Results in UI
```

## Technology Stack

### Backend
- **Python 3.8+**: Runtime
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **ChromaDB**: Vector database
- **Sentence Transformers**: Embedding generation
- **Pydantic**: Data validation

### Android
- **Kotlin**: Programming language
- **Jetpack Compose**: UI framework
- **Material Design 3**: Design system
- **Retrofit**: HTTP client
- **Coroutines**: Async programming
- **StateFlow**: Reactive state management

## Security Considerations

1. **Network Security**
   - HTTPS recommended for production
   - Certificate pinning for Android app
   - CORS policy configuration

2. **Data Security**
   - Input validation using Pydantic
   - No hardcoded credentials
   - Secure storage recommendations

3. **API Security**
   - Rate limiting recommended
   - Authentication/Authorization for production
   - Security headers

See [SECURITY.md](SECURITY.md) for detailed security information.

## Scalability Considerations

### Current Limitations
- Single-process backend server
- Local file-based database
- No caching layer
- No load balancing

### Scaling Recommendations

1. **Backend Scaling**
   - Deploy multiple instances behind load balancer
   - Use distributed ChromaDB or migrate to Pinecone/Weaviate
   - Add Redis caching layer
   - Implement async task queue (Celery)

2. **Database Scaling**
   - Move to cloud-based vector database
   - Implement sharding for large datasets
   - Add read replicas

3. **Performance Optimization**
   - Cache embeddings
   - Batch processing for multiple queries
   - Use faster embedding models
   - Implement query result caching

## Integration with Local LLM

### Ollama Integration Flow

```
Query Request
    ↓
Retrieve Relevant Docs (RAG)
    ↓
Build Context Prompt
    ↓
Send to Ollama API
    ↓
Stream/Receive Response
    ↓
Return to Client
```

### Supported Models
- Llama 2 (7B, 13B, 70B)
- Mistral
- CodeLlama
- Any Ollama-compatible model

### Configuration
```python
# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# Model selection
MODEL = "llama2"  # or "mistral", "codellama", etc.
```

## Deployment Options

### 1. Local Development
- Backend: `python main.py`
- Android: Android Studio emulator/device
- Network: Local network (WiFi)

### 2. Cloud Deployment

**Backend Options:**
- Google Cloud Run
- AWS Lambda + API Gateway
- Heroku
- DigitalOcean App Platform

**Database Options:**
- Pinecone (vector database)
- Weaviate (self-hosted or cloud)
- Qdrant
- Milvus

**Android Deployment:**
- Google Play Store
- Internal distribution
- Firebase App Distribution

### 3. Hybrid Deployment
- Backend in cloud
- Android app on devices
- Sync via REST API

## Monitoring and Observability

### Recommended Tools
1. **Application Monitoring**
   - Sentry for error tracking
   - New Relic for APM
   - Datadog for metrics

2. **Logging**
   - Structured logging (loguru)
   - Centralized logging (ELK stack)
   - Log rotation and retention

3. **Metrics**
   - Request latency
   - Error rates
   - Database query performance
   - Embedding generation time

## Future Enhancements

1. **Features**
   - User authentication
   - Multi-user support
   - Budget tracking
   - Financial analytics
   - Receipt OCR
   - Export functionality

2. **Technical**
   - GraphQL API option
   - WebSocket for real-time updates
   - Offline mode for Android
   - Data synchronization
   - Background processing

3. **AI/ML**
   - Fine-tuned embeddings for finance
   - Custom LLM training
   - Anomaly detection
   - Predictive analytics
   - Automated categorization

## Contributing

See the main README.md for contribution guidelines.

## License

This project is open source under the MIT License.
