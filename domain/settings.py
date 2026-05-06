from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    groq_api_key: str
    model_name: str = "llama-3.3-70b-versatile"
    embedding_model: str = "models/embedding-001"
    chunk_size: int = 500
    chunk_overlap: int = 50
    max_pages: int = 10

    model_config = SettingsConfigDict(env_file=".env")
    
settings= Settings()

