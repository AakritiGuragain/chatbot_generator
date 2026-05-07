from abc import ABC, abstractmethod
from domain.entities.website import WebsiteInput, WebsiteSession

class IngestPort(ABC):
    @abstractmethod
    def ingest(self, input: WebsiteInput) -> WebsiteSession:
        ...