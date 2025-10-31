#!/bin/bash

# Setup script for RAG Finance Tracking Backend

echo "Setting up RAG Finance Tracking Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version:"
python3 --version

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To start the backend server:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the server: python main.py"
echo ""
echo "The API will be available at http://localhost:8000"
echo "API documentation: http://localhost:8000/docs"
