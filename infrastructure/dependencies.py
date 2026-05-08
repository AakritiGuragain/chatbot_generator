from src.adapters.outbound.bs4_scanner import BS4Scanner
from src.adapters.outbound.ollama_embedder import OllamaEmbedder
from src.adapters.outbound.faiss_store import FAISSStore
from src.adapters.outbound.groq_llm import GroqLLM
from src.application.services.ingest_service import IngestService
from src.application.services.chat_service import ChatService

def build_ingest_service() -> IngestService:
    return IngestService(
        scanner=BS4Scanner(),
        embedder=OllamaEmbedder(),
        vector_store=FAISSStore(),
    )

def build_chat_service() -> ChatService:
    return ChatService(
        embedder=OllamaEmbedder(),
        vector_store=FAISSStore(),
        llm=GroqLLM(),
    )