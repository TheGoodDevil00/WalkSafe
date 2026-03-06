import os
from databases import Database
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/safewalk"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Use databases for async support
database = Database(settings.DATABASE_URL)
