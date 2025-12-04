"""Listening session model for tracking plays."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func

from app.database import Base


class ListeningSession(Base):
    """Model for storing individual listening sessions."""
    
    __tablename__ = "listening_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    track_id = Column(String, nullable=False, index=True)
    track_name = Column(String, nullable=False)
    artist_name = Column(String, nullable=False)
    album_name = Column(String, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    played_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    __table_args__ = (
        Index('idx_user_played', 'user_id', 'played_at'),
        Index('idx_user_track', 'user_id', 'track_id'),
    )
    
    def __repr__(self) -> str:
        return f"<ListeningSession(id={self.id}, track='{self.track_name}', artist='{self.artist_name}')>"
