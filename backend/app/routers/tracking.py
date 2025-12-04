"""Tracking router for custom listening statistics."""

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
