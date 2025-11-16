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
* **Python 3.x** (if running manually)

---

## 1. Environment Setup (Recommended: Docker)

The easiest way to start the environment is with Docker Compose:

```bash
# Clone the repository
git clone https://github.com/mousekeys/RAG_finetuning.git
cd RAG_finetuning

# Build and run all services
docker-compose up --build
```

---

## 2. Manual Setup (Python)

If running directly via Python:

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
├── src/                      # Core source code for RAG, finetuning, and data processing
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker services configuration
├── server.py                 # Backend RAG/LLM server
├── streamlitUI.py            # Streamlit UI
├── README.md                 # Project documentation
└── .gitignore                # Git ignore rules
```

---

## Future Enhancements (To‑Dos)

Planned improvements include:

### 🔹 Context Richness

Migrate from basic JSON structures to **Structured Language Models (SLM)** for richer context.

### 🔹 Automated Record Finding

Implement automation to identify and fetch relevant records for improved UX.

### 🔹 Embedding Optimization

Explore using a **smaller embedding model** to reduce storage, since current text chunks are small.

### 🔹 Streamlined Finetuning Pipeline

Develop a fully automated script for the entire model finetuning lifecycle.

### 🔹 Multimodal Versatility

Finetune a multimodal model (e.g., **QwenVL**) for more general OCR and data extraction tasks.


