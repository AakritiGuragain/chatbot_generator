import chromadb
from src.ports.outbound.vector_store_port import VectorStorePort
from src.domain.entities.chunk import DocumentChunk

class ChromaStore(VectorStorePort):
    def __init__(self, persist_dir: str = "vector_stores"):
        self.client = chromadb.PersistentClient(path=persist_dir)

    def _collection(self, website_id: str):
        safe_id = website_id.replace(".", "_").replace("-", "_")
        return self.client.get_or_create_collection(name=safe_id)

    def save(self, website_id: str, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        collection = self._collection(website_id)
        collection.add(
            ids=[f"chunk_{c.chunk_index}" for c in chunks],
            embeddings=embeddings,
            documents=[c.content for c in chunks],
            metadatas=[{"source": c.source, "chunk_index": c.chunk_index} for c in chunks]
        )

    def search(self, website_id: str, query_embedding: list[float], top_k: int = 4) -> list[DocumentChunk]:
        collection = self._collection(website_id)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        chunks = []
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            chunks.append(DocumentChunk(
                content=doc,
                source=meta["source"],
                chunk_index=meta["chunk_index"]
            ))
        return chunks

    def exists(self, website_id: str) -> bool:
        safe_id = website_id.replace(".", "_").replace("-", "_")
        col = self.client.get_or_create_collection(name=safe_id)
        return col.count() > 0