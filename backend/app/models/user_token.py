"""User token model for storing Spotify OAuth tokens."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from app.database import Base


class UserToken(Base):
    """Model for storing user OAuth tokens for background tracking."""
    
    __tablename__ = "user_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, nullable=False, index=True)
    display_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    # OAuth tokens
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    token_expires_at = Column(DateTime, nullable=False)
    
    # Tracking settings
    tracking_enabled = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_tracked_at = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        return f"<UserToken(user_id='{self.user_id}', display_name='{self.display_name}')>"
    
    @property
    def is_token_expired(self) -> bool:
        """Check if the access token is expired."""
        return datetime.utcnow() >= self.token_expires_at
