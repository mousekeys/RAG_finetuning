# Development Guide

This guide is for developers who want to contribute to or customize the RAG Finance Tracking system.

## Development Environment Setup

### Backend Development

1. **Install Development Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-asyncio black flake8 mypy
   ```

2. **Code Formatting**:
   ```bash
   # Format code with black
   black main.py
   
   # Check with flake8
   flake8 main.py
   ```

3. **Type Checking**:
   ```bash
   mypy main.py
   ```

### Android Development

1. **Install Android Studio**: Download from [developer.android.com](https://developer.android.com/studio)

2. **SDK Setup**:
   - API Level 24 (minimum)
   - API Level 34 (target)

3. **Recommended Plugins**:
   - Kotlin
   - Android Gradle Plugin
   - Compose Preview

## Project Structure

```
RAG_financetracking/
├── main.py                     # Backend server
├── requirements.txt            # Python dependencies
├── test_basic.py              # Basic tests
├── load_sample_data.py        # Sample data loader
├── setup.sh                   # Setup script
├── README.md                  # Main documentation
├── QUICKSTART.md              # Quick start guide
├── EXAMPLES.md                # Usage examples
├── SECURITY.md                # Security documentation
├── ARCHITECTURE.md            # Architecture documentation
├── DEVELOPMENT.md             # This file
└── android_app/               # Android application
    ├── build.gradle           # App build config
    ├── settings.gradle        # Project settings
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/financetracking/rag/
        │   ├── MainActivity.kt          # Main activity
        │   ├── data/
        │   │   └── FinanceRepository.kt # Data layer
        │   ├── network/
        │   │   ├── ApiClient.kt         # HTTP client
        │   │   └── FinanceApiService.kt # API interface
        │   ├── viewmodel/
        │   │   └── FinanceViewModel.kt  # ViewModel
        │   └── ui/
        │       ├── FinanceScreen.kt     # Main UI
        │       └── theme/               # UI theme
        └── res/                         # Resources
```

## Making Changes

### Backend Changes

1. **Adding New Endpoints**:
   ```python
   @app.get("/new-endpoint")
   async def new_endpoint():
       return {"message": "New endpoint"}
   ```

2. **Modifying Data Models**:
   ```python
   class NewModel(BaseModel):
       field1: str
       field2: int
   ```

3. **Testing Changes**:
   ```bash
   # Start server
   python main.py
   
   # Test in another terminal
   curl http://localhost:8000/new-endpoint
   ```

### Android Changes

1. **Adding New UI Components**:
   ```kotlin
   @Composable
   fun NewComponent() {
       Text("New Component")
   }
   ```

2. **Adding API Methods**:
   ```kotlin
   // In FinanceApiService.kt
   @GET("/new-endpoint")
   suspend fun getNewData(): Response<NewDataResponse>
   
   // In FinanceRepository.kt
   suspend fun getNewData(): Result<NewData> = withContext(Dispatchers.IO) {
       // Implementation
   }
   
   // In FinanceViewModel.kt
   fun fetchNewData() {
       viewModelScope.launch {
           // Implementation
       }
   }
   ```

3. **Testing Changes**:
   - Build and run in Android Studio
   - Use Android Emulator or physical device
   - Check Logcat for errors

## Testing

### Backend Testing

1. **Manual Testing**:
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # Add document
   curl -X POST http://localhost:8000/documents/add \
     -H "Content-Type: application/json" \
     -d '{"text":"test","category":"Expense"}'
   ```

2. **Automated Testing**:
   ```bash
   python test_basic.py
   ```

3. **Interactive API Testing**:
   - Open http://localhost:8000/docs
   - Use Swagger UI to test endpoints

### Android Testing

1. **Manual Testing**:
   - Run app on emulator/device
   - Test each feature
   - Check UI responsiveness

2. **Unit Testing** (to be implemented):
   ```kotlin
   @Test
   fun testViewModel() {
       // Test implementation
   }
   ```

## Common Development Tasks

### 1. Change API Base URL

**Backend**: Update port in `main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed port
```

**Android**: Update `ApiClient.kt`:
```kotlin
private const val BASE_URL = "http://10.0.2.2:8001/"  // New port
```

### 2. Add New Document Category

**Backend**: No changes needed (categories are dynamic)

**Android**: Update `AddDocumentTab` in `FinanceScreen.kt`:
```kotlin
val categories = listOf("Income", "Expense", "Investment", "Savings", "Loan", "Other", "NewCategory")
```

### 3. Customize UI Theme

Update `android_app/src/main/java/com/financetracking/rag/ui/theme/Color.kt`:
```kotlin
val Primary = Color(0xFF1976D2)  // Change primary color
val Secondary = Color(0xFF03DAC6)  // Change secondary color
```

### 4. Add Database Fields

**Backend**: Update `DocumentInput` in `main.py`:
```python
class DocumentInput(BaseModel):
    text: str
    category: str
    amount: Optional[float] = None
    date: Optional[str] = None
    metadata: Optional[dict] = {}
    new_field: Optional[str] = None  # Add new field
```

**Android**: Update `DocumentInput` in `FinanceApiService.kt`:
```kotlin
data class DocumentInput(
    val text: String,
    val category: String,
    val amount: Double? = null,
    val date: String? = null,
    val metadata: Map<String, Any>? = null,
    val newField: String? = null  // Add new field
)
```

## Debugging

### Backend Debugging

1. **Print Statements**:
   ```python
   print(f"Debug: {variable}")
   ```

2. **Python Debugger**:
   ```python
   import pdb; pdb.set_trace()
   ```

3. **Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   logging.debug("Debug message")
   ```

### Android Debugging

1. **Logcat**:
   ```kotlin
   import android.util.Log
   Log.d("FinanceApp", "Debug message")
   ```

2. **Android Studio Debugger**:
   - Set breakpoints in code
   - Run in Debug mode (Shift+F9)
   - Step through code

3. **Compose Preview**:
   ```kotlin
   @Preview
   @Composable
   fun PreviewFinanceScreen() {
       FinanceScreen()
   }
   ```

## Performance Optimization

### Backend

1. **Caching**:
   - Cache embeddings
   - Use Redis for session storage
   - Implement query result caching

2. **Database Optimization**:
   - Index frequently queried fields
   - Batch operations
   - Connection pooling

3. **Async Processing**:
   - Use background tasks for heavy operations
   - Implement task queues (Celery)

### Android

1. **Memory Management**:
   - Use `remember` in Compose
   - Avoid memory leaks
   - Use LazyColumn for lists

2. **Network Optimization**:
   - Implement retry logic
   - Cache API responses
   - Use OkHttp caching

3. **UI Performance**:
   - Minimize recompositions
   - Use derivedStateOf
   - Optimize images

## Code Style Guidelines

### Python

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions small and focused

Example:
```python
def process_document(text: str, category: str) -> dict:
    """
    Process a financial document.
    
    Args:
        text: The document text
        category: The document category
        
    Returns:
        Processed document dictionary
    """
    return {"text": text, "category": category}
```

### Kotlin

- Follow Kotlin conventions
- Use meaningful variable names
- Keep functions small
- Use Compose best practices

Example:
```kotlin
@Composable
fun DocumentCard(
    document: Document,
    modifier: Modifier = Modifier
) {
    Card(modifier = modifier) {
        Text(text = document.text)
    }
}
```

## Version Control

### Branching Strategy

- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches

### Commit Messages

Format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

Example:
```
feat: Add budget tracking feature
fix: Resolve API connection timeout
docs: Update README with deployment guide
```

## Deployment

### Backend Deployment

1. **Docker** (recommended):
   ```dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

2. **Cloud Platforms**:
   - Google Cloud Run
   - AWS Lambda
   - Heroku
   - DigitalOcean

### Android Deployment

1. **Build Release APK**:
   ```bash
   ./gradlew assembleRelease
   ```

2. **Generate Signed APK**:
   - Build → Generate Signed Bundle/APK
   - Follow the wizard

3. **Deploy to Play Store**:
   - Create developer account
   - Upload APK/Bundle
   - Complete store listing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Jetpack Compose Documentation](https://developer.android.com/jetpack/compose)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Kotlin Documentation](https://kotlinlang.org/docs/home.html)
- [Android Development](https://developer.android.com/)

## Getting Help

- Open an issue on GitHub
- Check existing documentation
- Review example code in EXAMPLES.md
- Read the architecture in ARCHITECTURE.md
