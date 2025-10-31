# Contributing to RAG Finance Tracking

Thank you for your interest in contributing to the RAG Finance Tracking system!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mousekeys/RAG_financetracking.git
   cd RAG_financetracking
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install in development mode**
   ```bash
   pip install -e .
   ```

## Code Structure

```
RAG_financetracking/
├── src/rag_system/      # Core RAG system modules
├── examples/            # Example scripts
├── tests/               # Unit tests
├── data/                # Document storage
└── README.md           # Documentation
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific tests:
```bash
python -m pytest tests/test_basic.py
```

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to all functions and classes
- Keep functions focused and modular

## Adding New Features

1. **Document Loaders**: Add new format support in `document_loader.py`
2. **Embeddings**: Extend `embeddings.py` for new embedding models
3. **Vector Stores**: Modify `vector_store.py` for different backends
4. **Configuration**: Update `config.py` for new settings

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add new feature'`)
7. Push to your fork (`git push origin feature/your-feature`)
8. Open a Pull Request

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## Questions?

Feel free to open an issue for questions or discussions!
