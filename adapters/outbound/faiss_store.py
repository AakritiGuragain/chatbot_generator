import os
import json
import faiss
import numpy as np
from ports.outbound.vector_store_port import VectorStorePort
from domain.entities.chunk import DocumentChunk

STORE_DIR = "vector_stores"

class FAISSStore(VectorStorePort):
    def save(self, website_id: str, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        path = self._path(website_id)
        os.makedirs(path, exist_ok=True)
        vectors = np.array(embeddings, dtype="float32")
        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors)
        faiss.write_index(index, f"{path}/index.faiss")
        with open(f"{path}/chunks.json", "w") as f:
            json.dump([c.model_dump() for c in chunks], f)

    def search(self, website_id: str, query_embedding: list[float], top_k: int = 4) -> list[DocumentChunk]:
        path = self._path(website_id)
        index = faiss.read_index(f"{path}/index.faiss")
        with open(f"{path}/chunks.json") as f:
            chunks_data = json.load(f)
        query = np.array([query_embedding], dtype="float32")
        _, indices = index.search(query, top_k)
        return [DocumentChunk(**chunks_data[i]) for i in indices[0] if i < len(chunks_data)]

    def exists(self, website_id: str) -> bool:
        return os.path.exists(f"{self._path(website_id)}/index.faiss")

    def _path(self, website_id: str) -> str:
        safe_id = website_id.replace("://", "_").replace("/", "_")
        return f"{STORE_DIR}/{safe_id}"