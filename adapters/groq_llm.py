from groq import Groq
from domain.ports.llm_port import LLMPort
from domain.settings import settings

class GroqLLM(LLMPort):
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def generate(self, question: str, context: str) -> str:
        prompt = f"""You are a helpful assistant for a website. 
Answer the user's question using ONLY the context below.
If the answer is not in the context, say "I couldn't find that information on this website."

Context:
{context}

Question: {question}
Answer:"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content