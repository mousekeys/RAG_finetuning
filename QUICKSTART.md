# Quick Start Guide

Get started with the RAG Finance Tracking System in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/mousekeys/RAG_financetracking.git
cd RAG_financetracking

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Using the Command Line Interface

```bash
# Load documents into the system
python cli.py load data/

# Query the system
python cli.py query "What is gross profit margin?"

# View statistics
python cli.py stats
```

### 2. Using Python Code

```python
from src.rag_system import RAGSystem

# Initialize the system
rag = RAGSystem()

# Load your documents
rag.load_documents("data/")

# Ask questions
result = rag.query("What are the main financial ratios?")
print(result['context'])
```

### 3. Run Example Scripts

```bash
# Basic usage example
python examples/basic_usage.py

# LLM integration example
python examples/llm_integration.py
```

## Adding Your Documents

1. Place your financial documents in the `data/` directory
2. Supported formats: PDF, DOCX, TXT
3. Run the load command to index them

```bash
python cli.py load data/
```

## Integration with Local LLMs

The RAG system retrieves relevant context that you can use with any local LLM:

```python
# Get context from RAG
result = rag.query("Your question here")

# Create prompt for your LLM
prompt = f"""
Context: {result['context']}
Question: {result['question']}
Answer:
"""

# Use with your preferred local LLM
# - llama-cpp-python
# - GPT4All
# - Ollama
# - etc.
```

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/llm_integration.py](examples/llm_integration.py) for LLM integration patterns
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

## Common Issues

**Problem**: ModuleNotFoundError
**Solution**: Make sure you've installed all dependencies with `pip install -r requirements.txt`

**Problem**: No documents found
**Solution**: Add documents to the `data/` directory before loading

**Problem**: Slow first run
**Solution**: The embedding model downloads on first use (this is normal)

## Get Help

- Check the [README.md](README.md) for full documentation
- Open an issue on GitHub for bugs or questions
- See examples in the `examples/` directory
