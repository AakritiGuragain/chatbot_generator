from abc import ABC, abstractmethod
from domain.models import DocumentChunk

class ScannerPort(ABC):
    @abstractmethod
    def scan(self, url: str, max_pages: int) -> list[DocumentChunk]:
        """Scan a website and return chunks of text"""
        