# RAG Finetuning for Data Analysis

## Overview

This repository provides an end-to-end implementation of **Retrieval-Augmented Generation (RAG)** and **Large Language Model (LLM) finetuning** tailored for **data analysis tasks**. It is designed to work with **custom, domain-specific data**, with a particular focus on processing and analyzing **image-based documents** (e.g., bank statements) through **Finetuned OCR** and **vector retrieval**.

The system integrates **ChromaDB** for vector storage and retrieval, includes scripts for serving the LLM backend, and provides an interactive UI via **Streamlit**.

## Features

* **RAG Implementation**: Uses **ChromaDB** for efficient vector storage and retrieval, enabling accurate responses using domain-specific data.
* **LLM Finetuning**: Includes components and scripts for finetuning an LLM to improve performance on complex data analysis tasks.
* **Multimodal Capability**: Supports OCR-based preprocessing for image documents. Chosen over QwenVL due to performance and runtime considerations.
* **Optimized Model Usage**: Utilizes **DeepSeek‑R1:8B** for fast inference combined with ChromaDB.
* **Containerized Setup**: Includes a `docker-compose.yml` for easy environment setup and deployment.
* **Interactive UI**: A Streamlit interface (`streamlitUI.py`) for querying the RAG system.

## Getting Started

Follow the steps below to run the project locally.

---

## Prerequisites

You will need:

* **Docker** and **Docker Compose** (recommended)
* **Python 3.11** (recommended)

---

## 1. Environment Setup (Recommended: Docker)

The chromadb is intialized using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/mousekeys/RAG_finetuning.git
cd RAG_finetuning

docker-compose up --build
```

---

## 2. Manual Setup (Python)

To run the UI and backend:

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Backend and UI

Use separate terminals:

```bash
# Terminal 1: Start backend
python server.py

# Terminal 2: Start Streamlit UI
streamlit run streamlitUI.py
```

---

## Project Structure

```
RAG_finetuning/
├── src/
│   ├── __pycache__/
│   ├── core/
│   │   ├── __pycache__/
│   │   ├── __init__.py         # Core package initialization
│   │   ├── db_client.py        # Database client (likely ChromaDB connection management)
│   │   ├── embedder.py         # Handles running the embedding model
│   │   ├── generator.py        # Logic for generating the final response using the LLM
│   │   ├── layout.py           # Functions related to document layout analysis (multimodal/OCR prep)
│   │   ├── pipeline.py         # The main RAG execution flow
│   │   └── retriever.py        # Logic for fetching relevant documents from the vector store
│   ├── models/
│   │   ├── __pycache__/
│   │   └── base.py             # Base classes or configurations for LLMs/other models
│   └── ocr/
│       ├── __pycache__/
│       ├── ocr_models/         # Directory for various OCR model implementations or configs
│       ├── __init__.py
│       ├── bbox.py             # Bounding box processing for OCR output
│       ├── kvp_extract.py      # Key-Value Pair (KVP) extraction logic from OCR results
│       ├── ocr_finetune.py     # Script/module for finetuning the OCR/extraction pipeline
│       └── ocrsurya.py         # Specific module likely implementing the 'Surya' OCR/layout model
├── requirements.txt          # Python dependencies.
├── docker-compose.yml        # Docker setup file for environment configuration.
├── server.py                 # Backend application (main entry point for the API server).
├── streamlitUI.py            # Streamlit application for the user interface.
├── README.md                 # Project documentation.
└── .gitignore                # Files/directories to ignore in version control.

```

---

## Future Enhancements (To‑Dos)

Planned improvements include:

### 1. Context Richness

Migrate from basic JSON structures to **Structured Language Models (SLM)** for richer context.

### 2. Automated Record Finding

Implement automation to identify and fetch relevant records for improved UX.

### 3. Embedding Optimization

Explore using a **smaller embedding model** to reduce storage, since current text chunks are small.

### 4. Streamlined Finetuning Pipeline

Develop a fully automated script for the entire model finetuning lifecycle.

### 5. Multimodal Versatility

Finetune a multimodal model (e.g., **QwenVL**) for more general OCR and data extraction tasks.


