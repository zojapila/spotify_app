"""Tracking service for custom listening statistics."""

from datetime import datetime, timedelta
from typing import Optional
from collections import Counter
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.listening_session import ListeningSession
from app.schemas.tracking import (
    RecordPlayRequest,
    RecordPlayResponse,
    TrackingStats,
    TrackingHistory,
    ListeningSessionResponse,
    TrackPlayCount,
    ArtistPlayCount,
    AlbumPlayCount,
)


class TrackingService:
    """Service for tracking and analyzing listening history."""
    
    def __init__(self, db: AsyncSession, user_id: str):
        self.db = db
        self.user_id = user_id
    
    async def record_play(self, request: RecordPlayRequest) -> RecordPlayResponse:
        """
        Record a play session.
        
        Prevents duplicates by checking if the same track was played
        in the last 3 minutes.
        """
        # Check for recent duplicate
        three_minutes_ago = datetime.utcnow() - timedelta(minutes=3)
        
        query = select(ListeningSession).where(
            and_(
                ListeningSession.user_id == self.user_id,
                ListeningSession.track_id == request.track_id,
                ListeningSession.played_at >= three_minutes_ago,
            )
        )
        
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            return RecordPlayResponse(
                message="Duplicate play detected, skipped",
                recorded=False,
            )
        
        # Create new session
        session = ListeningSession(
            user_id=self.user_id,
            track_id=request.track_id,
            track_name=request.track_name,
            artist_name=request.artist_name,
            album_name=request.album_name,
            duration_ms=request.duration_ms,
        )
        
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        
        return RecordPlayResponse(
            id=session.id,
            message="Listening session recorded",
            recorded=True,
        )
    
    async def get_stats(self, days: int = 30) -> TrackingStats:
        """Get listening statistics for a given period."""
        if days > 0:
            start_date = datetime.utcnow() - timedelta(days=days)
            date_filter = ListeningSession.played_at >= start_date
        else:
            date_filter = True  # No filter - all time
        
        # Base query for user's sessions
        base_query = select(ListeningSession).where(
            and_(
                ListeningSession.user_id == self.user_id,
                date_filter,
            )
        )
        
        result = await self.db.execute(base_query)
        sessions = result.scalars().all()
        
        if not sessions:
            return TrackingStats(
                period_days=days,
                total_plays=0,
                total_time_ms=0,
                total_time_formatted="0m",
                unique_tracks=0,
                unique_artists=0,
                unique_albums=0,
                average_daily_time_ms=0,
                average_daily_time_formatted="0m",
                top_tracks=[],
                top_artists=[],
                top_albums=[],
            )
        
        # Calculate statistics
        total_plays = len(sessions)
        total_time_ms = sum(s.duration_ms for s in sessions)
        
        unique_tracks = len(set(s.track_id for s in sessions))
        unique_artists = len(set(s.artist_name for s in sessions))
        unique_albums = len(set(s.album_name for s in sessions))
        
        # Average daily time
        actual_days = max(days, 1) if days > 0 else max((datetime.utcnow() - min(s.played_at for s in sessions)).days, 1)
        average_daily_time_ms = total_time_ms // actual_days
        
        # Top tracks
        track_counts: Counter = Counter()
        track_times: dict[str, int] = {}
        track_info: dict[str, dict] = {}
        
        for s in sessions:
            track_counts[s.track_id] += 1
            track_times[s.track_id] = track_times.get(s.track_id, 0) + s.duration_ms
            if s.track_id not in track_info:
                track_info[s.track_id] = {
                    "track_id": s.track_id,
                    "track_name": s.track_name,
                    "artist_name": s.artist_name,
                    "album_name": s.album_name,
                }
        
        top_tracks = [
            TrackPlayCount(
                **track_info[track_id],
                play_count=count,
                total_time_ms=track_times[track_id],
            )
            for track_id, count in track_counts.most_common(10)
        ]
        
        # Top artists
        artist_counts: Counter = Counter()
        artist_times: dict[str, int] = {}
        
        for s in sessions:
            artist_counts[s.artist_name] += 1
            artist_times[s.artist_name] = artist_times.get(s.artist_name, 0) + s.duration_ms
        
        top_artists = [
            ArtistPlayCount(
                artist_name=artist,
                play_count=count,
                total_time_ms=artist_times[artist],
            )
            for artist, count in artist_counts.most_common(10)
        ]
        
        # Top albums
        album_counts: Counter = Counter()
        album_times: dict[str, int] = {}
        album_artist: dict[str, str] = {}
        
        for s in sessions:
            album_counts[s.album_name] += 1
            album_times[s.album_name] = album_times.get(s.album_name, 0) + s.duration_ms
            album_artist[s.album_name] = s.artist_name
        
        top_albums = [
            AlbumPlayCount(
                album_name=album,
                artist_name=album_artist[album],
                play_count=count,
                total_time_ms=album_times[album],
            )
            for album, count in album_counts.most_common(10)
        ]
        
        return TrackingStats(
            period_days=days,
            total_plays=total_plays,
            total_time_ms=total_time_ms,
            total_time_formatted=self._format_time(total_time_ms),
            unique_tracks=unique_tracks,
            unique_artists=unique_artists,
            unique_albums=unique_albums,
            average_daily_time_ms=average_daily_time_ms,
            average_daily_time_formatted=self._format_time(average_daily_time_ms),
            top_tracks=top_tracks,
            top_artists=top_artists,
            top_albums=top_albums,
        )
    
    async def get_history(
        self,
        days: int = 30,
        limit: int = 100,
        offset: int = 0,
    ) -> TrackingHistory:
        """Get listening history."""
        if days > 0:
            start_date = datetime.utcnow() - timedelta(days=days)
            date_filter = ListeningSession.played_at >= start_date
        else:
            date_filter = True
        
        # Count total
        count_query = select(func.count()).select_from(ListeningSession).where(
            and_(
                ListeningSession.user_id == self.user_id,
                date_filter,
            )
        )
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Get items
        query = (
            select(ListeningSession)
            .where(
                and_(
                    ListeningSession.user_id == self.user_id,
                    date_filter,
                )
            )
            .order_by(ListeningSession.played_at.desc())
            .offset(offset)
            .limit(limit)
        )
        
        result = await self.db.execute(query)
        sessions = result.scalars().all()
        
        items = [
            ListeningSessionResponse(
                id=s.id,
                track_id=s.track_id,
                track_name=s.track_name,
                artist_name=s.artist_name,
                album_name=s.album_name,
                duration_ms=s.duration_ms,
                played_at=s.played_at,
            )
            for s in sessions
        ]
        
        return TrackingHistory(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
        )
    
    @staticmethod
    def _format_time(ms: int) -> str:
        """Format milliseconds to human readable string."""
        total_seconds = ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
