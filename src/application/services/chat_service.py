from src.ports.inbound.chat_port import ChatPort
from src.ports.outbound.embedder_port import EmbedderPort
from src.ports.outbound.vector_store_port import VectorStorePort
from src.ports.outbound.llm_port import LLMPort

class ChatService(ChatPort):
    def __init__(self, embedder: EmbedderPort, vector_store: VectorStorePort, llm: LLMPort):
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm = llm

    def chat(self, website_id: str, question: str) -> dict:
        if not self.vector_store.exists(website_id):
            raise ValueError(f"No chatbot found for {website_id}. Ingest first.")

        query_embedding = self.embedder.embed([question])[0]
        chunks = self.vector_store.search(website_id, query_embedding, top_k=4)
        context = "\n\n".join([c.content for c in chunks])
        sources = list(set([c.source for c in chunks]))
        answer = self.llm.generate(question, context)

        return {"answer": answer, "sources": sources}