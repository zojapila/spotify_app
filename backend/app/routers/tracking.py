"""Tracking router for custom listening statistics."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.database import get_db
from app.services.tracking_service import TrackingService
from app.services.spotify_service import SpotifyService
from app.schemas.tracking import (
    RecordPlayRequest,
    RecordPlayResponse,
    TrackingStats,
    TrackingHistory,
    AdvancedAnalytics,
    MonthlyComparison,
)

router = APIRouter(prefix="/api/tracking", tags=["tracking"])


async def get_user_id(authorization: str = Header(...)) -> str:
    """Get user ID from Spotify using access token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization[7:]
    service = SpotifyService(token)
    
    try:
        user = await service.get_current_user()
        return user.id
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=401, detail="Invalid access token")


@router.post("/record", response_model=RecordPlayResponse)
async def record_play(
    request: RecordPlayRequest,
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Record a play session."""
    service = TrackingService(db, user_id)
    return await service.record_play(request)


@router.get("/stats", response_model=TrackingStats)
async def get_stats(
    days: int = 30,
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get tracking statistics.
    
    Args:
        days: Number of days to include (0 = all time)
    """
    service = TrackingService(db, user_id)
    return await service.get_stats(days=days)


@router.get("/history", response_model=TrackingHistory)
async def get_history(
    days: int = 30,
    limit: int = 100,
    offset: int = 0,
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get listening history from tracking database.
    
    Args:
        days: Number of days to include (0 = all time)
        limit: Maximum number of items to return
        offset: Offset for pagination
    """
    service = TrackingService(db, user_id)
    return await service.get_history(days=days, limit=limit, offset=offset)


@router.get("/analytics", response_model=AdvancedAnalytics)
async def get_analytics(
    days: int = 30,
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get advanced listening analytics.
    
    Includes:
    - Daily listening breakdown
    - Hourly distribution (when do you listen most?)
    - Weekday distribution
    - Listening streaks
    - Trends (compared to previous period)
    - New artists discovered
    - Variety score
    
    Args:
        days: Number of days to analyze (0 = all time)
    """
    service = TrackingService(db, user_id)
    return await service.get_advanced_analytics(days=days)


@router.get("/monthly", response_model=List[MonthlyComparison])
async def get_monthly_comparison(
    months: int = 6,
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get month-over-month comparison.
    
    Returns statistics for each of the last N months including:
    - Total plays and listening time
    - Unique artists and tracks
    - Top artist and track for each month
    
    Args:
        months: Number of months to compare (default 6)
    """
    service = TrackingService(db, user_id)
    return await service.get_monthly_comparison(months=months)
