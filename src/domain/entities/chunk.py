from pydantic import BaseModel, Field

class DocumentChunk(BaseModel):
    content: str = Field(..., description="The content of the chunk")
    source: str = Field(..., description="The source of the chunk")
    chunk_index: int = Field(..., description="The index of the chunk")
    