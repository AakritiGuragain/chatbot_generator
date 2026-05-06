from abc import ABC, abstractmethod
from domain.models import DocumentChunk

class VectorStorePort(ABC):
    @abstractmethod
    def save(self, website_id: str, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        """Save embeddings to the vector store"""


    @abstractmethod
    def search(self, website_id: str, query_embedding: list[float], top_k: int = 4) -> list[DocumentChunk]:
        """Find most relevant chunks for a query"""
    

    @abstractmethod
    def exists(self, website_id: str) -> bool:
        """Check if a chatbot already exists for this website"""
        