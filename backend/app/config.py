"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Spotify API
    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str = "http://127.0.0.1:8000/api/auth/callback"
    
    # App
    secret_key: str = "change-this-in-production"
    database_url: str = "sqlite+aiosqlite:///./spotify_stats.db"
    
    # Frontend
    frontend_url: str = "http://127.0.0.1:3000"
    
    # Spotify API URLs
    spotify_auth_url: str = "https://accounts.spotify.com/authorize"
    spotify_token_url: str = "https://accounts.spotify.com/api/token"
    spotify_api_base_url: str = "https://api.spotify.com/v1"
    
    # OAuth Scopes
    spotify_scopes: str = "user-read-private user-read-email user-top-read user-read-recently-played user-read-currently-playing"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
