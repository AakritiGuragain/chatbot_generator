from pydantic import BaseModel

class DocumentChunk(BaseModel):
    content: str
    source: str
    chunk_index: int