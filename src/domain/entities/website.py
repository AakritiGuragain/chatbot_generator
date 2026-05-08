from pydantic import BaseModel, HttpUrl, Field

class WebsiteInput(BaseModel):
    url: HttpUrl
    max_pages: int = 10

class WebsiteSession(BaseModel):
    website_id: str = Field(..., description="Unique identifier for the website session")
    company_name: str = Field(..., description="Derived company name from the website URL")
    chunks_indexed: int = Field(..., description="Number of document chunks indexed for this website")
    status: str = Field(..., description="Status of the website session, e.g., 'created', 'already_exists'")