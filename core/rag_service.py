from urllib.parse import urlparse
from domain.ports.scanner_port import ScannerPort
from domain.ports.embedder_port import EmbedderPort
from domain.ports.vector_store_port import VectorStorePort
from domain.ports.llm_port import LLMPort
from domain.models import WebsiteInput, ChatRequest, ChatResponse

class RAGService:
    def __init__(
        self,
        scanner: ScannerPort,
        embedder: EmbedderPort,
        vector_store: VectorStorePort,
        llm: LLMPort,
    ):
        self.scanner = scanner
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm = llm

    def generate_chatbot(self, input: WebsiteInput) -> dict:
        """Phase 1 — scrape website and build its index"""
        website_id = urlparse(str(input.url)).netloc

        # Skip if already built
        if self.vector_store.exists(website_id):
            return {
                "website_id": website_id,
                "status": "already_exists",
                "message": f"Chatbot for {website_id} already exists. Ready to chat!"
            }

        # Scrape
        print(f"Scanning {input.url}...")
        chunks = self.scanner.scan(str(input.url), input.max_pages)

        if not chunks:
            raise ValueError(f"No content could be extracted from {input.url}")

        # Embed
        print(f"Embedding {len(chunks)} chunks...")
        texts = [c.content for c in chunks]
        embeddings = self.embedder.embed(texts)

        # Store
        print(f"Saving index for {website_id}...")
        self.vector_store.save(website_id, chunks, embeddings)

        return {
            "website_id": website_id,
            "status": "created",
            "chunks_indexed": len(chunks),
            "message": f"Chatbot for {website_id} is ready!"
        }

    def chat(self, request: ChatRequest) -> ChatResponse:
        """Phase 2 — answer a question using the website's index"""
        if not self.vector_store.exists(request.website_id):
            raise ValueError(f"No chatbot found for {request.website_id}. Please generate it first.")

        # Embed the question
        query_embedding = self.embedder.embed([request.question])[0]

        # Retrieve relevant chunks
        relevant_chunks = self.vector_store.search(
            request.website_id,
            query_embedding,
            top_k=4
        )

        # Build context
        context = "\n\n".join([c.content for c in relevant_chunks])
        sources = list(set([c.source for c in relevant_chunks]))

        # Generate answer
        answer = self.llm.generate(request.question, context)

        return ChatResponse(
            answer=answer,
            sources=sources,
            website_id=request.website_id
        )