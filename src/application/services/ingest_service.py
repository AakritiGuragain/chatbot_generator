from urllib.parse import urlparse
from src.ports.inbound.ingest_port import IngestPort
from src.ports.outbound.scanner_port import ScannerPort
from src.ports.outbound.embedder_port import EmbedderPort
from src.ports.outbound.vector_store_port import VectorStorePort
from src.domain.entities.website import WebsiteInput, WebsiteSession

class IngestService(IngestPort):
    def __init__(self, scanner: ScannerPort, embedder: EmbedderPort, vector_store: VectorStorePort):
        self.scanner = scanner
        self.embedder = embedder
        self.vector_store = vector_store

    def ingest(self, input: WebsiteInput) -> WebsiteSession:
        website_id = urlparse(str(input.url)).netloc
        company_name = website_id.replace("www.", "")

        if self.vector_store.exists(website_id):
            return WebsiteSession(
                website_id=website_id,
                company_name=company_name,
                chunks_indexed=0,
                status="already_exists"
            )

        print(f"Scanning {input.url}...")
        chunks = self.scanner.scan(str(input.url), input.max_pages)

        if not chunks:
            raise ValueError(f"No content extracted from {input.url}")

        print(f"Embedding {len(chunks)} chunks...")
        embeddings = self.embedder.embed([c.content for c in chunks])

        print(f"Saving index for {website_id}...")
        self.vector_store.save(website_id, chunks, embeddings)

        return WebsiteSession(
            website_id=website_id,
            company_name=company_name,
            chunks_indexed=len(chunks),
            status="created"
        )