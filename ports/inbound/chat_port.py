from abc import ABC, abstractmethod

class ChatPort(ABC):
    @abstractmethod
    def chat(self, website_id: str, question: str) -> dict:
        ...