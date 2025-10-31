# RAG Finance Tracking - Usage Examples

## Quick Start Examples

### 1. Testing the Backend API

Once the backend is running (`python main.py`), you can test it with curl:

```bash
# Check health
curl http://localhost:8000/health

# Add a financial document
curl -X POST "http://localhost:8000/documents/add" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Monthly salary payment from ABC Corp",
    "category": "Income",
    "amount": 5000.00,
    "date": "2024-01-01"
  }'

# Add more examples
curl -X POST "http://localhost:8000/documents/add" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Grocery shopping at Whole Foods",
    "category": "Expense",
    "amount": 150.75,
    "date": "2024-01-05"
  }'

curl -X POST "http://localhost:8000/documents/add" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Electric bill payment",
    "category": "Expense",
    "amount": 89.99,
    "date": "2024-01-10"
  }'

# Query your finances
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are my total expenses?",
    "n_results": 10
  }'

# Check document count
curl http://localhost:8000/documents/count
```

### 2. Sample Financial Documents

Here are some example documents you can add to test the system:

**Income Examples:**
```json
{
  "text": "Freelance web development project payment",
  "category": "Income",
  "amount": 2500.00,
  "date": "2024-01-15"
}

{
  "text": "Investment dividend from stock portfolio",
  "category": "Income",
  "amount": 350.00,
  "date": "2024-01-20"
}
```

**Expense Examples:**
```json
{
  "text": "Monthly rent payment for apartment",
  "category": "Expense",
  "amount": 1200.00,
  "date": "2024-01-01"
}

{
  "text": "Car insurance premium",
  "category": "Expense",
  "amount": 180.00,
  "date": "2024-01-03"
}

{
  "text": "Restaurant dinner with clients",
  "category": "Expense",
  "amount": 85.50,
  "date": "2024-01-12"
}
```

**Investment Examples:**
```json
{
  "text": "Purchased 10 shares of AAPL stock",
  "category": "Investment",
  "amount": 1750.00,
  "date": "2024-01-08"
}

{
  "text": "401k monthly contribution",
  "category": "Investment",
  "amount": 500.00,
  "date": "2024-01-15"
}
```

### 3. Sample Queries

After adding documents, try these queries:

```bash
# Query about expenses
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What did I spend on groceries?"}'

# Query about income
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my income sources?"}'

# Query about investments
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me my investments"}'

# General financial summary
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Give me a summary of my finances"}'
```

### 4. Android App Testing Workflow

1. **Start the backend server**:
   ```bash
   python main.py
   ```

2. **Configure the Android app**:
   - If using emulator: Keep `BASE_URL = "http://10.0.2.2:8000/"`
   - If using physical device: Update to `http://YOUR_IP:8000/`

3. **Find your IP address** (for physical device):
   - Linux/Mac: `ifconfig` or `ip addr`
   - Windows: `ipconfig`

4. **Run the app**:
   - Open Android Studio
   - Open the `android_app` folder
   - Click Run (Shift+F10)

5. **Test the app**:
   - Add some sample documents using the "Add Document" tab
   - Switch to "Query" tab and ask questions
   - Observe the real-time responses

### 5. Integrating Ollama (Local LLM)

For more intelligent responses, integrate Ollama:

1. **Install and setup Ollama**:
   ```bash
   # Install
   curl https://ollama.ai/install.sh | sh
   
   # Pull a model
   ollama pull llama2
   
   # Start Ollama (in a separate terminal)
   ollama serve
   ```

2. **Test Ollama**:
   ```bash
   curl http://localhost:11434/api/generate -d '{
     "model": "llama2",
     "prompt": "What is RAG in AI?",
     "stream": false
   }'
   ```

3. **Update main.py** with the Ollama integration code shown in README.md

4. **Restart the backend** and test with more complex queries

### 6. Python Script for Bulk Data Import

Create a file `import_data.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

documents = [
    {
        "text": "Monthly salary from employer",
        "category": "Income",
        "amount": 5000.00,
        "date": "2024-01-01"
    },
    {
        "text": "Rent payment",
        "category": "Expense",
        "amount": 1200.00,
        "date": "2024-01-01"
    },
    # Add more documents...
]

for doc in documents:
    response = requests.post(f"{BASE_URL}/documents/add", json=doc)
    print(f"Added: {doc['text']} - Status: {response.status_code}")

print(f"\nTotal documents: {requests.get(f'{BASE_URL}/documents/count').json()['count']}")
```

Run it:
```bash
python import_data.py
```

### 7. Testing the API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

You can test all endpoints directly from the browser!

## Common Use Cases

### Personal Finance Tracking
- Log all daily expenses
- Track income sources
- Monitor investment portfolio
- Query spending patterns

### Business Finance
- Record business transactions
- Track client payments
- Monitor operational costs
- Generate financial insights

### Budget Management
- Add budget categories
- Track against budget limits
- Query overspending areas
- Get financial recommendations (with LLM integration)

## Tips for Better Results

1. **Be descriptive**: Add detailed descriptions to documents
2. **Use categories**: Consistent categorization helps with queries
3. **Include dates**: Date information improves temporal queries
4. **Add context**: More context = better RAG results
5. **Test queries**: Try various query phrasings to see what works best
