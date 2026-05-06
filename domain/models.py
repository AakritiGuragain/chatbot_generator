from pydantic import BaseModel, HttpUrl

class WebsiteInput(BaseModel):
    url: HttpUrl
    max_pages: int = 10

class DocumentChunk(BaseModel):
    content: str
    source: str
    chunk_index: int

class ChatRequest(BaseModel):
    question: str
    website_id: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    website_id: str