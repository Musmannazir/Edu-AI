"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "AI Learning Assistant"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./ai_learning_assistant.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    WHISPER_MODEL: str = "whisper-1"
    EMBEDDINGS_MODEL: str = "text-embedding-ada-002"
    SUMMARIZATION_MODEL: str = "gpt-4-turbo-preview"
    
    # Pinecone
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = ""
    PINECONE_INDEX_NAME: str = "learning-assistant"
    
    # YouTube
    YOUTUBE_API_KEY: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:3001"]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 104857600  # 100MB
    
    # AI Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Learning Analytics
    MIN_QUIZ_ACCURACY: float = 0.7
    WEAK_AREA_THRESHOLD: float = 0.6
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
