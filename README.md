# RAG Finance Tracking System with Android App

A complete finance tracking system that uses Retrieval-Augmented Generation (RAG) with a local LLM to answer queries about your financial documents. Includes a Python backend API and an Android mobile application.

## Architecture

### Backend (Python)
- **FastAPI**: REST API server
- **ChromaDB**: Vector database for document storage
- **Sentence Transformers**: For embedding generation
- **Local LLM Support**: Ready for integration with Ollama/Llama 2

### Android App (Kotlin)
- **Jetpack Compose**: Modern UI framework
- **Retrofit**: REST API client
- **Coroutines**: Asynchronous operations
- **MVVM Architecture**: Clean separation of concerns

## Features

### Backend API
- ✅ Add financial documents with metadata (category, amount, date)
- ✅ Query documents using semantic search
- ✅ Vector database storage with ChromaDB
- ✅ RESTful API endpoints
- ✅ CORS support for mobile apps
- 🔄 Local LLM integration (template included for Ollama)

### Android App
- ✅ Query financial documents
- ✅ Add new financial documents
- ✅ View document count
- ✅ Clear all documents
- ✅ Material Design 3 UI
- ✅ Dark/Light theme support
- ✅ Real-time status updates

## Setup Instructions

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the backend server**:
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

3. **Optional - Set up Ollama for local LLM**:
   ```bash
   # Install Ollama
   curl https://ollama.ai/install.sh | sh
   
   # Pull a model (e.g., Llama 2)
   ollama pull llama2
   
   # Start Ollama server
   ollama serve
   ```
   
   Then update the `_generate_answer` function in `main.py` to use Ollama.

### Android App Setup

1. **Prerequisites**:
   - Android Studio (Arctic Fox or later)
   - JDK 11 or later
   - Android SDK with API level 24+

2. **Open the project**:
   - Open Android Studio
   - Select "Open an existing project"
   - Navigate to the `android_app` folder

3. **Configure the backend URL**:
   - Open `android_app/src/main/java/com/financetracking/rag/network/ApiClient.kt`
   - Update `BASE_URL`:
     - For Android Emulator: `http://10.0.2.2:8000/` (localhost)
     - For Physical Device: `http://YOUR_COMPUTER_IP:8000/`

4. **Build and run**:
   - Click the "Run" button in Android Studio
   - Select your device or emulator
   - The app will install and launch automatically

## API Endpoints

### GET /
- **Description**: Root endpoint
- **Response**: API information

### GET /health
- **Description**: Health check
- **Response**: System status and timestamp

### POST /documents/add
- **Description**: Add a financial document
- **Request Body**:
  ```json
  {
    "text": "Grocery shopping at Walmart",
    "category": "Expense",
    "amount": 125.50,
    "date": "2024-01-15"
  }
  ```

### POST /query
- **Description**: Query financial documents
- **Request Body**:
  ```json
  {
    "query": "What are my expenses this month?",
    "n_results": 5
  }
  ```

### GET /documents/count
- **Description**: Get total document count

### DELETE /documents/clear
- **Description**: Clear all documents

## Usage Examples

### Adding Documents via API

```bash
curl -X POST "http://localhost:8000/documents/add" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Salary deposit from employer",
    "category": "Income",
    "amount": 5000.00,
    "date": "2024-01-01"
  }'
```

### Querying Documents via API

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me all my income sources",
    "n_results": 10
  }'
```

## Android App Usage

1. **Add Documents**:
   - Switch to "Add Document" tab
   - Fill in the description, category, amount, and date
   - Click "Add Document"

2. **Query Documents**:
   - Switch to "Query" tab
   - Enter your question about finances
   - Click "Query" to get results
   - View the answer and relevant documents

3. **Manage Documents**:
   - Document count is shown in the top bar
   - Use "Clear All Documents" to reset the database

## Integration with Local LLM

To enhance the RAG system with a local LLM (recommended for production):

1. **Install Ollama**:
   ```bash
   curl https://ollama.ai/install.sh | sh
   ```

2. **Pull a model**:
   ```bash
   ollama pull llama2  # or mistral, codellama, etc.
   ```

3. **Update the backend code**:
   Replace the `_generate_answer` function in `main.py`:
   
   ```python
   import requests
   
   def _generate_answer(query: str, relevant_docs: List[dict]) -> str:
       context = "\n".join([doc["text"] for doc in relevant_docs[:3]])
       
       prompt = f"""Based on the following financial documents, answer the question.
       
       Documents:
       {context}
       
       Question: {query}
       
       Answer:"""
       
       response = requests.post('http://localhost:11434/api/generate', 
           json={
               "model": "llama2",
               "prompt": prompt,
               "stream": False
           })
       
       return response.json()['response']
   ```

## Project Structure

```
RAG_financetracking/
├── main.py                 # FastAPI backend server
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── android_app/           # Android application
    ├── build.gradle       # App-level build configuration
    ├── settings.gradle    # Project settings
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/financetracking/rag/
        │   ├── MainActivity.kt
        │   ├── data/
        │   │   └── FinanceRepository.kt
        │   ├── network/
        │   │   ├── ApiClient.kt
        │   │   └── FinanceApiService.kt
        │   ├── viewmodel/
        │   │   └── FinanceViewModel.kt
        │   └── ui/
        │       ├── FinanceScreen.kt
        │       └── theme/
        │           ├── Color.kt
        │           ├── Theme.kt
        │           └── Type.kt
        └── res/
            ├── values/
            │   ├── strings.xml
            │   └── themes.xml
            └── xml/
                ├── backup_rules.xml
                └── data_extraction_rules.xml
```

## Technology Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern web framework
- **ChromaDB** - Vector database
- **Sentence Transformers** - Embedding generation
- **Uvicorn** - ASGI server

### Android
- **Kotlin** - Programming language
- **Jetpack Compose** - UI framework
- **Material Design 3** - Design system
- **Retrofit** - HTTP client
- **Coroutines** - Async programming
- **ViewModel** - State management

## Future Enhancements

- [ ] Full Ollama integration with streaming responses
- [ ] User authentication and multi-user support
- [ ] Data persistence on mobile app
- [ ] Budget tracking and analytics
- [ ] Receipt image upload and OCR
- [ ] Export data to CSV/PDF
- [ ] Push notifications for budget alerts
- [ ] Offline mode for Android app
- [ ] Advanced query filters
- [ ] Financial report generation

## Troubleshooting

### Backend Issues

**Problem**: ChromaDB initialization fails
- **Solution**: Delete the `chroma_db` folder and restart the server

**Problem**: Port 8000 already in use
- **Solution**: Change the port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`

### Android Issues

**Problem**: Cannot connect to backend
- **Solution**: 
  - Ensure backend is running
  - Check `BASE_URL` in `ApiClient.kt`
  - For physical device, use computer's IP address, not localhost

**Problem**: Build errors
- **Solution**: 
  - File → Invalidate Caches / Restart
  - Update Gradle dependencies
  - Sync project with Gradle files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on the GitHub repository.