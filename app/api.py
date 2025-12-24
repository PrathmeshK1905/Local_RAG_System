# app/api.py

from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

from app.ingest import load_pdf
from app.chunker import chunk_text
from app.embedder import Embedder
from app.retriever import Retriever
from app.prompt import build_prompt
from app.llm import generate_answer

app = FastAPI(title="Local RAG System")

DATA_DIR = Path("data/raw_docs")
INDEX_DIR = Path("embeddings/faiss_index")

DATA_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DIR.mkdir(parents=True, exist_ok=True)

embedder = Embedder()
retriever = Retriever(
    embedding_dim=384,  # MiniLM embedding size
    index_path=INDEX_DIR
)

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    if not file or not file.filename:
        return {"error": "No file uploaded"}

    file_path = DATA_DIR / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = load_pdf(file_path)

    if not text.strip():
        return {"error": "No text extracted from document"}

    chunks = chunk_text(text)

    if not chunks:
        return {"error": "Document could not be chunked"}

    embeddings = embedder.embed(chunks)
    retriever.add(embeddings, chunks)

    return {
        "status": "document ingested",
        "chunks": len(chunks)
    }


@app.post("/query")
async def query_document(question: str):
    query_embedding = embedder.embed([question])
    retrieved_chunks = retriever.search(query_embedding)

    context = "\n\n".join(retrieved_chunks)
    prompt = build_prompt(context, question)

    answer = generate_answer(prompt)

    if "Not found in provided documents" in answer:
        return {
            "question": question,
            "answer": "Not found in provided documents"
        }


    return {
        "question": question,
        "answer": answer
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
