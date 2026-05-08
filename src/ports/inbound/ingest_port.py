from abc import ABC, abstractmethod
from src.domain.entities.website import WebsiteInput, WebsiteSession

class IngestPort(ABC):
    @abstractmethod
    def ingest(self, input: WebsiteInput) -> WebsiteSession:
        ...