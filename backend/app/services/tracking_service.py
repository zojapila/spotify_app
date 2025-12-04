"""Tracking service for custom listening statistics."""

from datetime import datetime, timedelta
from typing import Optional
from collections import Counter, defaultdict
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
    AdvancedAnalytics,
    DailyListening,
    HourlyDistribution,
    WeekdayDistribution,
    ListeningStreak,
    ListeningTrend,
    ArtistDiscovery,
    MonthlyComparison,
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
    
    async def get_advanced_analytics(self, days: int = 30) -> AdvancedAnalytics:
        """Get advanced analytics for a given period."""
        if days > 0:
            start_date = datetime.utcnow() - timedelta(days=days)
            date_filter = ListeningSession.played_at >= start_date
        else:
            start_date = None
            date_filter = True
        
        # Get all sessions for period
        query = select(ListeningSession).where(
            and_(
                ListeningSession.user_id == self.user_id,
                date_filter,
            )
        ).order_by(ListeningSession.played_at)
        
        result = await self.db.execute(query)
        sessions = result.scalars().all()
        
        if not sessions:
            return self._empty_analytics()
        
        # Daily listening
        daily_data: dict[str, dict] = defaultdict(lambda: {"plays": 0, "time_ms": 0})
        hourly_data: dict[int, dict] = defaultdict(lambda: {"plays": 0, "time_ms": 0})
        weekday_data: dict[int, dict] = defaultdict(lambda: {"plays": 0, "time_ms": 0})
        
        all_dates = set()
        track_first_seen: dict[str, datetime] = {}
        artist_first_seen: dict[str, datetime] = {}
        
        for s in sessions:
            date_str = s.played_at.strftime("%Y-%m-%d")
            hour = s.played_at.hour
            weekday = s.played_at.weekday()
            
            daily_data[date_str]["plays"] += 1
            daily_data[date_str]["time_ms"] += s.duration_ms
            
            hourly_data[hour]["plays"] += 1
            hourly_data[hour]["time_ms"] += s.duration_ms
            
            weekday_data[weekday]["plays"] += 1
            weekday_data[weekday]["time_ms"] += s.duration_ms
            
            all_dates.add(s.played_at.date())
            
            # Track first seen dates
            if s.track_id not in track_first_seen:
                track_first_seen[s.track_id] = s.played_at
            if s.artist_name not in artist_first_seen:
                artist_first_seen[s.artist_name] = s.played_at
        
        # Build daily listening list
        daily_listening = []
        if start_date:
            current = start_date.date()
            end = datetime.utcnow().date()
        else:
            current = min(s.played_at.date() for s in sessions)
            end = datetime.utcnow().date()
        
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            data = daily_data.get(date_str, {"plays": 0, "time_ms": 0})
            daily_listening.append(DailyListening(
                date=date_str,
                plays=data["plays"],
                time_ms=data["time_ms"],
                time_formatted=self._format_time(data["time_ms"]),
            ))
            current += timedelta(days=1)
        
        # Hourly distribution
        total_plays = len(sessions)
        hourly_distribution = []
        for hour in range(24):
            data = hourly_data.get(hour, {"plays": 0, "time_ms": 0})
            hourly_distribution.append(HourlyDistribution(
                hour=hour,
                plays=data["plays"],
                time_ms=data["time_ms"],
                percentage=round(data["plays"] / total_plays * 100, 1) if total_plays > 0 else 0,
            ))
        
        # Weekday distribution
        weekday_names = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
        weekday_distribution = []
        for day_num in range(7):
            data = weekday_data.get(day_num, {"plays": 0, "time_ms": 0})
            weekday_distribution.append(WeekdayDistribution(
                day=weekday_names[day_num],
                day_number=day_num,
                plays=data["plays"],
                time_ms=data["time_ms"],
                percentage=round(data["plays"] / total_plays * 100, 1) if total_plays > 0 else 0,
            ))
        
        # Listening streak
        streak = self._calculate_streak(all_dates)
        
        # Trend (compare with previous period)
        trend = await self._calculate_trend(days)
        
        # New artists discovered in this period
        new_artists = await self._get_new_artists(sessions, days)
        
        # New tracks count
        if start_date:
            new_tracks_count = sum(1 for d in track_first_seen.values() if d >= start_date)
        else:
            new_tracks_count = len(track_first_seen)
        
        # Fun stats
        most_played_hour = max(hourly_data.keys(), key=lambda h: hourly_data[h]["plays"]) if hourly_data else 0
        most_played_day_num = max(weekday_data.keys(), key=lambda d: weekday_data[d]["plays"]) if weekday_data else 0
        
        total_time_ms = sum(s.duration_ms for s in sessions)
        average_track_length_ms = total_time_ms // len(sessions) if sessions else 0
        
        # Variety score (based on unique artists / total plays ratio)
        unique_artists = len(set(s.artist_name for s in sessions))
        variety_score = min(100, round(unique_artists / len(sessions) * 100 * 5, 1)) if sessions else 0
        
        return AdvancedAnalytics(
            daily_listening=daily_listening,
            hourly_distribution=hourly_distribution,
            weekday_distribution=weekday_distribution,
            streak=streak,
            trend=trend,
            new_artists=new_artists,
            new_tracks_count=new_tracks_count,
            most_played_hour=most_played_hour,
            most_played_day=weekday_names[most_played_day_num],
            average_track_length_ms=average_track_length_ms,
            listening_variety_score=variety_score,
        )
    
    def _calculate_streak(self, dates: set) -> ListeningStreak:
        """Calculate listening streak."""
        if not dates:
            return ListeningStreak(current_streak=0, longest_streak=0, last_listen_date=None)
        
        sorted_dates = sorted(dates)
        last_date = sorted_dates[-1]
        today = datetime.utcnow().date()
        
        # Current streak (counting from today backwards)
        current_streak = 0
        check_date = today
        while check_date in dates or check_date == today:
            if check_date in dates:
                current_streak += 1
            check_date -= timedelta(days=1)
            if check_date < sorted_dates[0]:
                break
        
        # Longest streak
        longest_streak = 0
        current_run = 0
        prev_date = None
        
        for d in sorted_dates:
            if prev_date is None or (d - prev_date).days == 1:
                current_run += 1
            else:
                longest_streak = max(longest_streak, current_run)
                current_run = 1
            prev_date = d
        
        longest_streak = max(longest_streak, current_run)
        
        return ListeningStreak(
            current_streak=current_streak,
            longest_streak=longest_streak,
            last_listen_date=last_date.strftime("%Y-%m-%d"),
        )
    
    async def _calculate_trend(self, days: int) -> ListeningTrend:
        """Calculate trend comparing current vs previous period."""
        if days <= 0:
            return ListeningTrend(
                current_period_ms=0,
                previous_period_ms=0,
                change_percentage=0,
                trend="stable",
            )
        
        now = datetime.utcnow()
        current_start = now - timedelta(days=days)
        previous_start = current_start - timedelta(days=days)
        
        # Current period
        current_query = select(func.sum(ListeningSession.duration_ms)).where(
            and_(
                ListeningSession.user_id == self.user_id,
                ListeningSession.played_at >= current_start,
            )
        )
        result = await self.db.execute(current_query)
        current_ms = result.scalar() or 0
        
        # Previous period
        previous_query = select(func.sum(ListeningSession.duration_ms)).where(
            and_(
                ListeningSession.user_id == self.user_id,
                ListeningSession.played_at >= previous_start,
                ListeningSession.played_at < current_start,
            )
        )
        result = await self.db.execute(previous_query)
        previous_ms = result.scalar() or 0
        
        # Calculate change
        if previous_ms > 0:
            change = ((current_ms - previous_ms) / previous_ms) * 100
        elif current_ms > 0:
            change = 100
        else:
            change = 0
        
        if change > 5:
            trend = "up"
        elif change < -5:
            trend = "down"
        else:
            trend = "stable"
        
        return ListeningTrend(
            current_period_ms=current_ms,
            previous_period_ms=previous_ms,
            change_percentage=round(change, 1),
            trend=trend,
        )
    
    async def _get_new_artists(self, sessions: list, days: int) -> list[ArtistDiscovery]:
        """Get artists discovered in this period."""
        if not sessions or days <= 0:
            return []
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all artists user ever listened to before this period
        old_query = select(ListeningSession.artist_name).where(
            and_(
                ListeningSession.user_id == self.user_id,
                ListeningSession.played_at < start_date,
            )
        ).distinct()
        
        result = await self.db.execute(old_query)
        old_artists = set(row[0] for row in result.fetchall())
        
        # Find new artists in current period
        new_artist_data: dict[str, dict] = {}
        
        for s in sessions:
            if s.artist_name not in old_artists:
                if s.artist_name not in new_artist_data:
                    new_artist_data[s.artist_name] = {
                        "first_listen": s.played_at,
                        "plays": 0,
                        "time_ms": 0,
                    }
                new_artist_data[s.artist_name]["plays"] += 1
                new_artist_data[s.artist_name]["time_ms"] += s.duration_ms
        
        # Sort by plays and return top 10
        sorted_artists = sorted(
            new_artist_data.items(),
            key=lambda x: x[1]["plays"],
            reverse=True,
        )[:10]
        
        return [
            ArtistDiscovery(
                artist_name=name,
                first_listen=data["first_listen"],
                total_plays=data["plays"],
                total_time_ms=data["time_ms"],
            )
            for name, data in sorted_artists
        ]
    
    async def get_monthly_comparison(self, months: int = 6) -> list[MonthlyComparison]:
        """Get month over month comparison."""
        comparisons = []
        
        now = datetime.utcnow()
        
        for i in range(months):
            # Calculate month boundaries
            if now.month - i > 0:
                year = now.year
                month = now.month - i
            else:
                year = now.year - 1
                month = 12 + (now.month - i)
            
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            # Query for this month
            query = select(ListeningSession).where(
                and_(
                    ListeningSession.user_id == self.user_id,
                    ListeningSession.played_at >= start_date,
                    ListeningSession.played_at < end_date,
                )
            )
            
            result = await self.db.execute(query)
            sessions = result.scalars().all()
            
            if sessions:
                total_time_ms = sum(s.duration_ms for s in sessions)
                unique_artists = set(s.artist_name for s in sessions)
                unique_tracks = set(s.track_id for s in sessions)
                
                # Top artist and track
                artist_counts = Counter(s.artist_name for s in sessions)
                track_counts = Counter((s.track_id, s.track_name) for s in sessions)
                
                top_artist = artist_counts.most_common(1)[0][0] if artist_counts else None
                top_track = track_counts.most_common(1)[0][0][1] if track_counts else None
            else:
                total_time_ms = 0
                unique_artists = set()
                unique_tracks = set()
                top_artist = None
                top_track = None
            
            comparisons.append(MonthlyComparison(
                month=f"{year}-{month:02d}",
                total_plays=len(sessions),
                total_time_ms=total_time_ms,
                total_time_formatted=self._format_time(total_time_ms),
                unique_artists=len(unique_artists),
                unique_tracks=len(unique_tracks),
                top_artist=top_artist,
                top_track=top_track,
            ))
        
        return comparisons
    
    def _empty_analytics(self) -> AdvancedAnalytics:
        """Return empty analytics when no data."""
        return AdvancedAnalytics(
            daily_listening=[],
            hourly_distribution=[HourlyDistribution(hour=h, plays=0, time_ms=0, percentage=0) for h in range(24)],
            weekday_distribution=[
                WeekdayDistribution(day=d, day_number=i, plays=0, time_ms=0, percentage=0)
                for i, d in enumerate(["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"])
            ],
            streak=ListeningStreak(current_streak=0, longest_streak=0, last_listen_date=None),
            trend=ListeningTrend(current_period_ms=0, previous_period_ms=0, change_percentage=0, trend="stable"),
            new_artists=[],
            new_tracks_count=0,
            most_played_hour=0,
            most_played_day="Brak danych",
            average_track_length_ms=0,
            listening_variety_score=0,
        )
