"""Tracking schemas for custom statistics."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RecordPlayRequest(BaseModel):
    """Request to record a play."""
    track_id: str
    track_name: str
    artist_name: str
    album_name: str
    duration_ms: int


class RecordPlayResponse(BaseModel):
    """Response after recording a play."""
    id: Optional[int] = None
    message: str
    recorded: bool = True


class TrackPlayCount(BaseModel):
    """Track with play count."""
    track_id: str
    track_name: str
    artist_name: str
    album_name: str
    play_count: int
    total_time_ms: int


class ArtistPlayCount(BaseModel):
    """Artist with play count."""
    artist_name: str
    play_count: int
    total_time_ms: int


class AlbumPlayCount(BaseModel):
    """Album with play count."""
    album_name: str
    artist_name: str
    play_count: int
    total_time_ms: int


class TrackingStats(BaseModel):
    """User's tracking statistics."""
    period_days: int
    total_plays: int
    total_time_ms: int
    total_time_formatted: str
    unique_tracks: int
    unique_artists: int
    unique_albums: int
    average_daily_time_ms: int
    average_daily_time_formatted: str
    top_tracks: List[TrackPlayCount]
    top_artists: List[ArtistPlayCount]
    top_albums: List[AlbumPlayCount]


class ListeningSessionResponse(BaseModel):
    """Single listening session response."""
    id: int
    track_id: str
    track_name: str
    artist_name: str
    album_name: str
    duration_ms: int
    played_at: datetime


class TrackingHistory(BaseModel):
    """Tracking history response."""
    items: List[ListeningSessionResponse]
    total: int
    limit: int
    offset: int
