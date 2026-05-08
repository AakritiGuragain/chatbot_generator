from groq import Groq
from typing import Generator
from src.ports.outbound.llm_port import LLMPort
from infrastructure.settings import settings

class GroqLLM(LLMPort):
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def generate(self, question: str, context: str) -> str:
        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[{"role": "user", "content": self._prompt(question, context)}],
            temperature=0.3,
        )
        return response.choices[0].message.content

    def generate_stream(self, question: str, context: str) -> Generator:
        stream = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[{"role": "user", "content": self._prompt(question, context)}],
            temperature=0.3,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def _prompt(self, question: str, context: str) -> str:
        return f"""You are a helpful assistant for a website.
Answer using ONLY the context below.
If the answer is not in the context, say "I couldn't find that information on this website."

Context:
{context}

Question: {question}
Answer:"""