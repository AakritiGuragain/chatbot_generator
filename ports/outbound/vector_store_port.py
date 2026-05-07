from abc import ABC, abstractmethod
from domain.entities.chunk import DocumentChunk

class VectorStorePort(ABC):
    @abstractmethod
    def save(self, website_id: str, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        ...

    @abstractmethod
    def search(self, website_id: str, query_embedding: list[float], top_k: int = 4) -> list[DocumentChunk]:
        ...

    @abstractmethod
    def exists(self, website_id: str) -> bool:
        ...