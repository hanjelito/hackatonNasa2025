from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"

    # Google AI Configuration
    API_KEY_VERTEXAI: str = "DEFAULT_API_KEY"

    # Load environment variables from a .env file
    model_config = SettingsConfigDict(env_file=".env")


# Load settings and cache them
@lru_cache
def get_settings() -> Settings:
    return Settings()


# Easy access to the setting
settings = get_settings()