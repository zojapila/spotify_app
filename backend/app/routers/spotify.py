"""Spotify data router."""

from typing import Literal
from fastapi import APIRouter, HTTPException, Header
import httpx

from app.services.spotify_service import SpotifyService
from app.schemas.spotify import (
    SpotifyUser,
    TopArtistsResponse,
    TopTracksResponse,
    TopAlbumsResponse,
    RecentlyPlayedResponse,
)

router = APIRouter(prefix="/api/spotify", tags=["spotify"])

TimeRange = Literal["short_term", "medium_term", "long_term"]


def get_access_token(authorization: str = Header(...)) -> str:
    """Extract access token from Authorization header."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return authorization[7:]  # Remove "Bearer " prefix


@router.get("/me", response_model=SpotifyUser)
async def get_current_user(authorization: str = Header(...)):
    """Get current user's Spotify profile."""
    token = get_access_token(authorization)
    service = SpotifyService(token)
    
    try:
        return await service.get_current_user()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to get user profile")


@router.get("/top/artists", response_model=TopArtistsResponse)
async def get_top_artists(
    authorization: str = Header(...),
    time_range: TimeRange = "medium_term",
    limit: int = 20,
    offset: int = 0,
):
    """Get user's top artists."""
    token = get_access_token(authorization)
    service = SpotifyService(token)
    
    try:
        return await service.get_top_artists(
            time_range=time_range,
            limit=limit,
            offset=offset,
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to get top artists")


@router.get("/top/tracks", response_model=TopTracksResponse)
async def get_top_tracks(
    authorization: str = Header(...),
    time_range: TimeRange = "medium_term",
    limit: int = 20,
    offset: int = 0,
):
    """Get user's top tracks."""
    token = get_access_token(authorization)
    service = SpotifyService(token)
    
    try:
        return await service.get_top_tracks(
            time_range=time_range,
            limit=limit,
            offset=offset,
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to get top tracks")


@router.get("/top/albums", response_model=TopAlbumsResponse)
async def get_top_albums(
    authorization: str = Header(...),
    time_range: TimeRange = "medium_term",
    limit: int = 20,
):
    """Get user's top albums (calculated from top tracks)."""
    token = get_access_token(authorization)
    service = SpotifyService(token)
    
    try:
        return await service.get_top_albums(
            time_range=time_range,
            limit=limit,
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to get top albums")


@router.get("/recently-played", response_model=RecentlyPlayedResponse)
async def get_recently_played(
    authorization: str = Header(...),
    limit: int = 20,
):
    """Get user's recently played tracks."""
    token = get_access_token(authorization)
    service = SpotifyService(token)
    
    try:
        return await service.get_recently_played(limit=limit)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to get recently played")
