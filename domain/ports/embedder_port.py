from abc import ABC, abstractmethod

class EmbedderPort(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Convert text chunks into vectors"""
        