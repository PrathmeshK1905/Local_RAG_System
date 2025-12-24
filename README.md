# Local RAG System (Offline)

A simple, production-style **Retrieval-Augmented Generation (RAG)** system built using **Ollama (Llama 3.1)**, **FAISS**, and **FastAPI**, running fully **offline** with persistent vector storage.

---

## Features
- Local LLM inference via Ollama
- PDF ingestion and text chunking
- FAISS-based vector search (persistent)
- Context-grounded answers (hallucination-safe)
- FastAPI backend
- Basic evaluation script

---

## Tech Stack
- Python
- FastAPI
- Ollama (Llama 3.1)
- FAISS
- Sentence Transformers

---

## Run
```bash
ollama run llama3.1
uvicorn app.api:app --host 127.0.0.1 --port 8000
Swagger UI:

dts
Copy code
http://127.0.0.1:8000/docs
Evaluation
bash
Copy code
python evaluation/evaluator.py
Author
Prathmesh Amol Kulkarni
