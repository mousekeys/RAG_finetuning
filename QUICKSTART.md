# Quick Start Guide

Get up and running with the RAG Finance Tracking system in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Android Studio (for Android app development)
- Git

## Backend Setup (5 minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/mousekeys/RAG_financetracking.git
cd RAG_financetracking
```

### 2. Install Dependencies

**Option A: Using the setup script (Linux/Mac)**
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

**Option B: Manual installation**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start the Backend Server

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Test the API

Open another terminal and test:
```bash
# Health check
curl http://localhost:8000/health

# Expected output:
# {"status":"healthy","timestamp":"2024-01-15T10:30:00.000000"}
```

View the interactive API docs at: http://localhost:8000/docs

## Android App Setup (5 minutes)

### 1. Open in Android Studio

1. Launch Android Studio
2. Select "Open an existing project"
3. Navigate to `RAG_financetracking/android_app`
4. Click "OK"

### 2. Configure Backend URL

The default configuration works for Android Emulator. For a physical device:

1. Find your computer's IP address:
   ```bash
   # Linux/Mac
   ifconfig | grep inet
   
   # Windows
   ipconfig
   ```

2. Update the URL in `android_app/src/main/java/com/financetracking/rag/network/ApiClient.kt`:
   ```kotlin
   private const val BASE_URL = "http://YOUR_IP_ADDRESS:8000/"
   ```

### 3. Build and Run

1. Click the "Run" button (green triangle) or press Shift+F10
2. Select your emulator or connected device
3. Wait for the build to complete and app to launch

## First Steps

### Add Your First Document

1. In the Android app, tap the "Add Document" tab
2. Fill in:
   - **Description**: "Monthly salary from employer"
   - **Category**: Select "Income"
   - **Amount**: 5000
   - **Date**: 2024-01-01
3. Tap "Add Document"
4. You should see a success message

### Add More Documents

Add a few more for testing:

**Expense Example:**
- Description: "Grocery shopping at Whole Foods"
- Category: Expense
- Amount: 150.75
- Date: 2024-01-05

**Investment Example:**
- Description: "Purchased 10 shares of AAPL"
- Category: Investment
- Amount: 1750
- Date: 2024-01-08

### Query Your Finances

1. Switch to the "Query" tab
2. Enter a question: "What are my expenses?"
3. Tap "Query"
4. View the results and relevant documents

## Using the API Directly

You can also use the API without the Android app:

### Add a Document
```bash
curl -X POST "http://localhost:8000/documents/add" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Restaurant dinner with clients",
    "category": "Expense",
    "amount": 85.50,
    "date": "2024-01-12"
  }'
```

### Query Documents
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What did I spend money on?",
    "n_results": 5
  }'
```

### Check Document Count
```bash
curl http://localhost:8000/documents/count
```

## Troubleshooting

### Backend Won't Start

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Make sure you activated the virtual environment and installed dependencies

**Problem**: `Address already in use`
**Solution**: Another process is using port 8000. Change the port in `main.py` or kill the other process

### Android App Can't Connect

**Problem**: "Connection failed" error in the app
**Solution**: 
1. Ensure the backend is running
2. Check the BASE_URL is correct
3. For emulator, use `http://10.0.2.2:8000/`
4. For physical device, use your computer's IP address
5. Make sure your phone and computer are on the same network

**Problem**: Build errors in Android Studio
**Solution**:
1. File → Invalidate Caches / Restart
2. Build → Clean Project
3. Build → Rebuild Project

### Embedding Model Download

**Problem**: "Could not load embedding model" warning
**Solution**: The model needs to download on first run (requires internet). It's about 90MB and will be cached after the first download.

## Next Steps

1. **Explore the Documentation**
   - Read [README.md](README.md) for full documentation
   - Check [EXAMPLES.md](EXAMPLES.md) for more usage examples
   - Review [SECURITY.md](SECURITY.md) before deploying to production
   - See [ARCHITECTURE.md](ARCHITECTURE.md) for system architecture

2. **Integrate a Local LLM**
   - Install Ollama: `curl https://ollama.ai/install.sh | sh`
   - Pull a model: `ollama pull llama2`
   - Update the `_generate_answer` function in `main.py` (see README.md)

3. **Customize for Your Needs**
   - Add more categories
   - Customize the UI
   - Add authentication
   - Deploy to production

## Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check the documentation files
- **Security**: See [SECURITY.md](SECURITY.md) for security reporting

## Summary

You now have:
- ✅ A running RAG backend server
- ✅ An Android app connected to the backend
- ✅ Added financial documents
- ✅ Queried documents using natural language

Enjoy tracking your finances with AI! 🚀
