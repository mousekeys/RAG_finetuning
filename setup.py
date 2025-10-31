"""
Setup configuration for RAG Finance Tracking System.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="rag-financetracking",
    version="0.1.0",
    author="RAG Finance Tracking Contributors",
    description="A RAG system for financial document processing with local LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mousekeys/RAG_financetracking",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.13",
        "chromadb>=0.4.22",
        "sentence-transformers>=2.3.1",
        "pypdf>=4.0.0",
        "python-docx>=1.1.0",
        "openpyxl>=3.1.2",
        "llama-cpp-python>=0.2.27",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)
