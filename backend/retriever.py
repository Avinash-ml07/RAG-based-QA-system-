import faiss
import numpy as np
from backend.embeddings import EmbeddingModel


class PolicyRetriever:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.index = None
        self.chunks = []

    def build_index(self, chunks: list[str]):
        self.chunks = chunks
        embeddings = self.embedder.encode(chunks)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def retrieve(self, query: str, top_k: int = 3):
        if not self.index:
            raise RuntimeError("Index not built")

        query_vec = self.embedder.encode([query])
        distances, indices = self.index.search(query_vec, top_k)

        return [self.chunks[i] for i in indices[0]]
