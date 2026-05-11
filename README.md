# Instant Website Chatbot Generator

A RAG-based system that takes any website URL and instantly generates a working chatbot trained on that website's content — no manual setup, no fine-tuning required.

---

## What It Does

Enter any company website URL → the system scrapes it, builds a knowledge base, and gives you a chatbot that can answer questions about that website in real time.

```
https://veelapp.com  →  "What is Veel?" → "Veel is a platform for UGC campaigns..."
```

---

## Tech Stack

| Component | Tool |
|---|---|
| Language | Python 3.11 |
| Architecture | Hexagonal (Ports & Adapters) |
| LLM | LLaMA 3.3 70B via Groq API |
| Embeddings | nomic-embed-text via Ollama (local) |
| Vector DB | ChromaDB |
| Scraper | requests + BeautifulSoup |
| UI | Streamlit (streaming responses) |
| Package Manager | uv |

---

## Architecture

This project follows **Hexagonal Architecture (Ports & Adapters)**:

```
src/
├── domain/          ← core business objects (no external dependencies)
├── ports/           ← abstract interfaces (inbound + outbound)
├── application/     ← use case logic (orchestrates ports)
└── adapters/        ← concrete implementations (Streamlit, BS4, Ollama, ChromaDB, Groq)

infrastructure/      ← settings + composition root (wires everything together)
```

The domain core never imports from adapters. Swapping any tool (e.g. Groq → OpenAI, ChromaDB → Pinecone) requires changing only `infrastructure/dependencies.py`.

---

## How It Works

### Phase 1 — Ingestion
```
URL → scrape pages → extract text → chunk (150 words) → embed (768-dim) → save to ChromaDB
```

### Phase 2 — Chat
```
Question → embed → search ChromaDB → top 4 chunks → Groq LLM → streaming response
```

---

## Prerequisites

- macOS (Apple Silicon) or Linux
- Python 3.11 via Homebrew
- [uv](https://astral.sh/uv) — package manager
- [Ollama](https://ollama.com) — local embedding model
- [Groq API key](https://console.groq.com) — free tier available

---

## Setup

```bash
# Clone the repo
git clone https://github.com/AakritiGuragain/chatbot_generator.git
cd chatbot_generator

# Install dependencies
uv sync

# Add your Groq API key
echo 'GROQ_API_KEY=your_key_here' > .env

# Pull the embedding model
ollama pull nomic-embed-text
```

---

## Run

```bash
./run.sh
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

1. Enter any website URL (e.g. `https://veelapp.com`)
2. Click **⚡ Generate Chatbot**
3. Wait for scraping and indexing to complete
4. Ask questions — answers stream word by word

To generate a chatbot for a different website, click **🔄 New**.

---

## Project Structure

```
chatbot_generator/
├── src/
│   ├── domain/
│   │   └── entities/
│   │       ├── chunk.py              # DocumentChunk model
│   │       └── website.py            # WebsiteInput, WebsiteSession models
│   ├── ports/
│   │   ├── inbound/
│   │   │   ├── ingest_port.py        # contract for URL ingestion
│   │   │   └── chat_port.py          # contract for chat
│   │   └── outbound/
│   │       ├── scanner_port.py       # contract for web scraping
│   │       ├── embedder_port.py      # contract for embeddings
│   │       ├── vector_store_port.py  # contract for vector DB
│   │       └── llm_port.py           # contract for LLM
│   ├── application/
│   │   └── services/
│   │       ├── ingest_service.py     # Phase 1 use case
│   │       └── chat_service.py       # Phase 2 use case
│   └── adapters/
│       ├── inbound/
│       │   └── streamlit_adapter.py  # Streamlit UI
│       └── outbound/
│           ├── bs4_scanner.py        # web scraper
│           ├── ollama_embedder.py    # local embeddings
│           ├── chroma_store.py       # vector storage
│           └── groq_llm.py           # LLM + streaming
├── infrastructure/
│   ├── settings.py                   # Pydantic config
│   └── dependencies.py               # composition root
├── main.py
├── run.sh
├── pyproject.toml
└── .env.example
```

---

## Limitations

- Works best on static websites — JS-heavy sites (React, Vue) may not scrape well
- Cannot access content behind login walls
- Ollama must be running locally before launching the app
- Groq free tier has rate limits

---

## Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Never commit `.env` to Git — it is listed in `.gitignore`.

---

## Acknowledgements

- [Groq](https://groq.com) — fast LLM inference
- [Ollama](https://ollama.com) — local embedding models
- [ChromaDB](https://www.trychroma.com) — vector database
- [Streamlit](https://streamlit.io) — UI framework