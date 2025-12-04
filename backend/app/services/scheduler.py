"""Background scheduler for automatic tracking."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker
from app.models.user_token import UserToken
from app.models.listening_session import ListeningSession
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Global scheduler instance
scheduler: Optional[AsyncIOScheduler] = None


async def refresh_access_token(user_token: UserToken, db: AsyncSession) -> Optional[str]:
    """Refresh the access token using refresh token."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.spotify_token_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": user_token.refresh_token,
                    "client_id": settings.spotify_client_id,
                    "client_secret": settings.spotify_client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to refresh token for user {user_token.user_id}: {response.text}")
                return None
            
            tokens = response.json()
            
            # Update token in database
            user_token.access_token = tokens["access_token"]
            user_token.token_expires_at = datetime.utcnow() + timedelta(seconds=tokens["expires_in"])
            
            # Update refresh token if provided (Spotify sometimes rotates it)
            if "refresh_token" in tokens:
                user_token.refresh_token = tokens["refresh_token"]
            
            await db.commit()
            
            logger.info(f"Refreshed token for user {user_token.user_id}")
            return tokens["access_token"]
            
        except Exception as e:
            logger.error(f"Error refreshing token for user {user_token.user_id}: {e}")
            return None


async def get_currently_playing(access_token: str) -> Optional[dict]:
    """Fetch currently playing track from Spotify API."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.spotify_api_base_url}/me/player/currently-playing",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            
            if response.status_code == 204:
                # No content - nothing playing
                return None
            
            if response.status_code == 200:
                data = response.json()
                if data and data.get("is_playing") and data.get("item"):
                    return data["item"]
            
            return None
            
        except Exception as e:
            logger.debug(f"Error fetching currently playing: {e}")
            return None


async def record_play_if_new(
    db: AsyncSession,
    user_id: str,
    track: dict,
) -> bool:
    """Record a play if it's not a duplicate (same track in last 3 minutes)."""
    track_id = track["id"]
    three_minutes_ago = datetime.utcnow() - timedelta(minutes=3)
    
    # Check for recent duplicate
    query = select(ListeningSession).where(
        ListeningSession.user_id == user_id,
        ListeningSession.track_id == track_id,
        ListeningSession.played_at >= three_minutes_ago,
    )
    
    result = await db.execute(query)
    existing = result.scalar_one_or_none()
    
    if existing:
        return False  # Duplicate, skip
    
    # Extract track info
    artists = ", ".join(a["name"] for a in track.get("artists", []))
    album = track.get("album", {})
    
    # Create new session
    session = ListeningSession(
        user_id=user_id,
        track_id=track_id,
        track_name=track.get("name", "Unknown"),
        artist_name=artists or "Unknown",
        album_name=album.get("name", "Unknown"),
        duration_ms=track.get("duration_ms", 0),
    )
    
    db.add(session)
    await db.commit()
    
    logger.info(f"Recorded: {track.get('name')} by {artists} for user {user_id}")
    return True


async def track_all_users():
    """Main tracking job - check all users' currently playing tracks."""
    logger.debug("Running tracking job...")
    
    async with async_session_maker() as db:
        # Get all users with tracking enabled
        query = select(UserToken).where(UserToken.tracking_enabled == True)
        result = await db.execute(query)
        users = result.scalars().all()
        
        if not users:
            logger.debug("No users to track")
            return
        
        for user_token in users:
            try:
                # Check if token needs refresh
                access_token = user_token.access_token
                
                if user_token.is_token_expired:
                    access_token = await refresh_access_token(user_token, db)
                    if not access_token:
                        continue  # Skip this user if refresh failed
                
                # Get currently playing
                track = await get_currently_playing(access_token)
                
                if track:
                    await record_play_if_new(db, user_token.user_id, track)
                
                # Update last tracked timestamp
                user_token.last_tracked_at = datetime.utcnow()
                await db.commit()
                
            except Exception as e:
                logger.error(f"Error tracking user {user_token.user_id}: {e}")
                continue


def start_scheduler():
    """Start the background scheduler."""
    global scheduler
    
    if scheduler is not None:
        logger.warning("Scheduler already running")
        return
    
    scheduler = AsyncIOScheduler()
    
    # Run tracking every 30 seconds
    scheduler.add_job(
        track_all_users,
        trigger=IntervalTrigger(seconds=30),
        id="track_all_users",
        name="Track all users' currently playing",
        replace_existing=True,
    )
    
    scheduler.start()
    logger.info("🎵 Background tracking scheduler started (every 30s)")


def stop_scheduler():
    """Stop the background scheduler."""
    global scheduler
    
    if scheduler:
        scheduler.shutdown(wait=False)
        scheduler = None
        logger.info("Background tracking scheduler stopped")
