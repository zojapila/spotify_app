"""Spotify API service."""

from typing import Optional, Literal
from collections import Counter
import httpx

from app.config import get_settings
from app.schemas.spotify import (
    SpotifyUser,
    SpotifyArtist,
    SpotifyTrack,
    SpotifyAlbum,
    TopArtistsResponse,
    TopTracksResponse,
    TopAlbumsResponse,
    RecentlyPlayedResponse,
    PlayHistoryItem,
)

settings = get_settings()

TimeRange = Literal["short_term", "medium_term", "long_term"]


class SpotifyService:
    """Service for interacting with Spotify API."""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = settings.spotify_api_base_url
        self.headers = {"Authorization": f"Bearer {access_token}"}
    
    async def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make GET request to Spotify API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
    
    async def get_current_user(self) -> SpotifyUser:
        """Get current user profile."""
        data = await self._get("me")
        return SpotifyUser(**data)
    
    async def get_top_artists(
        self,
        time_range: TimeRange = "medium_term",
        limit: int = 20,
        offset: int = 0,
    ) -> TopArtistsResponse:
        """Get user's top artists."""
        data = await self._get(
            "me/top/artists",
            params={
                "time_range": time_range,
                "limit": min(limit, 50),
                "offset": offset,
            },
        )
        
        artists = [SpotifyArtist(**item) for item in data.get("items", [])]
        
        return TopArtistsResponse(
            items=artists,
            total=data.get("total", len(artists)),
            limit=limit,
            offset=offset,
            time_range=time_range,
        )
    
    async def get_top_tracks(
        self,
        time_range: TimeRange = "medium_term",
        limit: int = 20,
        offset: int = 0,
    ) -> TopTracksResponse:
        """Get user's top tracks."""
        data = await self._get(
            "me/top/tracks",
            params={
                "time_range": time_range,
                "limit": min(limit, 50),
                "offset": offset,
            },
        )
        
        tracks = [SpotifyTrack(**item) for item in data.get("items", [])]
        
        return TopTracksResponse(
            items=tracks,
            total=data.get("total", len(tracks)),
            limit=limit,
            offset=offset,
            time_range=time_range,
        )
    
    async def get_top_albums(
        self,
        time_range: TimeRange = "medium_term",
        limit: int = 20,
    ) -> TopAlbumsResponse:
        """
        Get user's top albums (calculated from top tracks).
        
        Spotify doesn't have a direct endpoint for top albums,
        so we calculate it based on top tracks.
        """
        # Get more tracks to have better album coverage
        tracks_response = await self.get_top_tracks(
            time_range=time_range,
            limit=50,
        )
        
        # Count albums by track appearances
        album_counts: Counter = Counter()
        album_data: dict[str, dict] = {}
        
        for track in tracks_response.items:
            album_id = track.album.id
            album_counts[album_id] += 1
            
            if album_id not in album_data:
                album_data[album_id] = {
                    "id": album_id,
                    "name": track.album.name,
                    "artists": [
                        {"id": a.id, "name": a.name, "external_urls": a.external_urls}
                        for a in track.artists
                    ],
                    "images": [img.model_dump() for img in track.album.images],
                    "release_date": track.album.release_date,
                    "external_urls": track.album.external_urls,
                    "track_count_in_top": 0,
                }
        
        # Build album list with counts
        albums = []
        for album_id, count in album_counts.most_common(limit):
            album_info = album_data[album_id]
            album_info["track_count_in_top"] = count
            albums.append(SpotifyAlbum(**album_info))
        
        return TopAlbumsResponse(
            items=albums,
            total=len(albums),
            limit=limit,
            time_range=time_range,
        )
    
    async def get_recently_played(self, limit: int = 20) -> RecentlyPlayedResponse:
        """Get recently played tracks."""
        data = await self._get(
            "me/player/recently-played",
            params={"limit": min(limit, 50)},
        )
        
        items = []
        for item in data.get("items", []):
            track = SpotifyTrack(**item["track"])
            items.append(PlayHistoryItem(
                track=track,
                played_at=item["played_at"],
            ))
        
        return RecentlyPlayedResponse(
            items=items,
            total=len(items),
        )
    
    async def get_currently_playing(self) -> Optional[SpotifyTrack]:
        """Get currently playing track (if any)."""
        try:
            data = await self._get("me/player/currently-playing")
            
            if data and data.get("item"):
                return SpotifyTrack(**data["item"])
            return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 204:
                # No content - nothing playing
                return None
            raise
