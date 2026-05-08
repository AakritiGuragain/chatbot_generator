from ollama import Client
from src.ports.outbound.embedder_port import EmbedderPort

class OllamaEmbedder(EmbedderPort):
    def __init__(self, model: str = "nomic-embed-text"):
        self.client = Client()
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            response = self.client.embeddings(
                model=self.model,
                prompt=text
            )
            embeddings.append(response["embedding"])
        return embeddings