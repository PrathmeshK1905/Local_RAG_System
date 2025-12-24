# app/retriever.py

import faiss
import numpy as np
from pathlib import Path
from typing import List

class Retriever:
    def __init__(self, embedding_dim: int, index_path: Path):
        self.index_path = index_path
        self.text_path = index_path / "chunks.npy"
        self.faiss_path = index_path / "index.faiss"

        index_path.mkdir(parents=True, exist_ok=True)

        if self.faiss_path.exists() and self.text_path.exists():
            self.index = faiss.read_index(str(self.faiss_path))
            self.text_chunks = np.load(self.text_path, allow_pickle=True).tolist()
        else:
            self.index = faiss.IndexFlatL2(embedding_dim)
            self.text_chunks: List[str] = []

    def add(self, embeddings: np.ndarray, chunks: List[str]):
        self.index.add(embeddings)
        self.text_chunks.extend(chunks)
        self._save()

    def search(self, query_embedding: np.ndarray, top_k: int = 10):
        if self.index.ntotal == 0:
            return []
        _, indices = self.index.search(query_embedding, top_k)
        return [self.text_chunks[i] for i in indices[0]]


    def _save(self):
        faiss.write_index(self.index, str(self.faiss_path))
        np.save(self.text_path, np.array(self.text_chunks, dtype=object))
