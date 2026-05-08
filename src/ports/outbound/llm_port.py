from abc import ABC, abstractmethod
from typing import Generator

class LLMPort(ABC):
    @abstractmethod
    def generate(self, question: str, context: str) -> str:
        ...

    @abstractmethod
    def generate_stream(self, question: str, context: str) -> Generator:
        ...