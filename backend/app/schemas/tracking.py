"""Tracking schemas for custom statistics."""

from pydantic import BaseModel
from typing import List, Optional, Dict
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


# ===== ADVANCED ANALYTICS SCHEMAS =====

class DailyListening(BaseModel):
    """Listening data for a single day."""
    date: str  # YYYY-MM-DD
    plays: int
    time_ms: int
    time_formatted: str


class HourlyDistribution(BaseModel):
    """Listening distribution by hour."""
    hour: int  # 0-23
    plays: int
    time_ms: int
    percentage: float


class WeekdayDistribution(BaseModel):
    """Listening distribution by day of week."""
    day: str  # Monday, Tuesday, etc.
    day_number: int  # 0=Monday, 6=Sunday
    plays: int
    time_ms: int
    percentage: float


class ListeningStreak(BaseModel):
    """Listening streak information."""
    current_streak: int
    longest_streak: int
    last_listen_date: Optional[str]


class ListeningTrend(BaseModel):
    """Trend comparison between periods."""
    current_period_ms: int
    previous_period_ms: int
    change_percentage: float
    trend: str  # "up", "down", "stable"


class ArtistDiscovery(BaseModel):
    """New artists discovered in period."""
    artist_name: str
    first_listen: datetime
    total_plays: int
    total_time_ms: int


class AdvancedAnalytics(BaseModel):
    """Advanced analytics response."""
    # Time-based analysis
    daily_listening: List[DailyListening]
    hourly_distribution: List[HourlyDistribution]
    weekday_distribution: List[WeekdayDistribution]
    
    # Streaks and trends
    streak: ListeningStreak
    trend: ListeningTrend
    
    # Discovery
    new_artists: List[ArtistDiscovery]
    new_tracks_count: int
    
    # Fun stats
    most_played_hour: int
    most_played_day: str
    average_track_length_ms: int
    listening_variety_score: float  # 0-100, how diverse is listening


class MonthlyComparison(BaseModel):
    """Month over month comparison."""
    month: str  # YYYY-MM
    total_plays: int
    total_time_ms: int
    total_time_formatted: str
    unique_artists: int
    unique_tracks: int
    top_artist: Optional[str]
    top_track: Optional[str]
