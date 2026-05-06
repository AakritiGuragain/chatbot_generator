from abc import ABC, abstractmethod

class LLMPort(ABC):
    @abstractmethod
    def generate(self, question: str, context: str) -> str:
        """Generate an answer given a question and retrieved context"""
        