from core.rag_service import RAGService
from adapters.bs4_scanner import BS4Scanner
from adapters.sentence_embedder import SimpleEmbedder
from adapters.faiss_store import FAISSStore
from adapters.groq_llm import GroqLLM
from domain.models import WebsiteInput, ChatRequest

def build_service() -> RAGService:
    return RAGService(
        scanner=BS4Scanner(),
        embedder=SimpleEmbedder(),
        vector_store=FAISSStore(),
        llm=GroqLLM(),
    )

if __name__ == "__main__":
    service = build_service()

    # Test with a real website
    url = input("Enter a website URL to generate chatbot for: ").strip()

    print("\nGenerating chatbot...")
    result = service.generate_chatbot(WebsiteInput(url=url))
    print(result)

    website_id = result["website_id"]

    print("\nChatbot ready! Type your questions (or 'quit' to exit)")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() == "quit":
            break

        response = service.chat(ChatRequest(
            question=question,
            website_id=website_id
        ))
        print(f"\nBot: {response.answer}")
        print(f"Sources: {response.sources}")