from abc import ABC, abstractmethod
from domain.entities.chunk import DocumentChunk

class ScannerPort(ABC):
    @abstractmethod
    def scan(self, url: str, max_pages: int) -> list[DocumentChunk]:
        ...