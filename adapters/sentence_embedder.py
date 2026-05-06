import hashlib
import math
from collections import Counter
from domain.ports.embedder_port import EmbedderPort

class SimpleEmbedder(EmbedderPort):
    def __init__(self, dim: int = 512):
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(t) for t in texts]

    def _embed_one(self, text: str) -> list[float]:
        words = text.lower().split()
        counts = Counter(words)
        vector = [0.0] * self.dim
        for word, count in counts.items():
            idx = int(hashlib.md5(word.encode()).hexdigest(), 16) % self.dim
            vector[idx] += math.log(1 + count)
        # Normalize
        norm = math.sqrt(sum(x*x for x in vector)) or 1.0
        return [x / norm for x in vector]