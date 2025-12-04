"""Spotify API response schemas."""

from pydantic import BaseModel
from typing import List, Optional


class SpotifyImage(BaseModel):
    """Spotify image object."""
    url: str
    height: Optional[int] = None
    width: Optional[int] = None


class SpotifyArtistSimple(BaseModel):
    """Simplified artist object."""
    id: str
    name: str
    external_urls: Optional[dict] = None


class SpotifyAlbumSimple(BaseModel):
    """Simplified album object."""
    id: str
    name: str
    images: List[SpotifyImage] = []
    release_date: Optional[str] = None
    external_urls: Optional[dict] = None


class SpotifyUser(BaseModel):
    """Spotify user profile."""
    id: str
    display_name: Optional[str] = None
    email: Optional[str] = None
    images: List[SpotifyImage] = []
    product: Optional[str] = None
    followers: Optional[dict] = None
    external_urls: Optional[dict] = None


class SpotifyArtist(BaseModel):
    """Full Spotify artist object."""
    id: str
    name: str
    genres: List[str] = []
    popularity: Optional[int] = None
    images: List[SpotifyImage] = []
    external_urls: Optional[dict] = None
    followers: Optional[dict] = None


class SpotifyTrack(BaseModel):
    """Spotify track object."""
    id: str
    name: str
    duration_ms: int
    popularity: Optional[int] = None
    album: SpotifyAlbumSimple
    artists: List[SpotifyArtistSimple]
    external_urls: Optional[dict] = None
    preview_url: Optional[str] = None


class SpotifyAlbum(BaseModel):
    """Full Spotify album object with track count."""
    id: str
    name: str
    artists: List[SpotifyArtistSimple]
    images: List[SpotifyImage] = []
    release_date: Optional[str] = None
    total_tracks: Optional[int] = None
    track_count_in_top: int = 0  # Custom field: how many tracks from this album are in user's top
    external_urls: Optional[dict] = None


class TopArtistsResponse(BaseModel):
    """Response for top artists endpoint."""
    items: List[SpotifyArtist]
    total: int
    limit: int
    offset: int
    time_range: str


class TopTracksResponse(BaseModel):
    """Response for top tracks endpoint."""
    items: List[SpotifyTrack]
    total: int
    limit: int
    offset: int
    time_range: str


class TopAlbumsResponse(BaseModel):
    """Response for top albums endpoint (calculated)."""
    items: List[SpotifyAlbum]
    total: int
    limit: int
    time_range: str


class PlayHistoryItem(BaseModel):
    """Item in play history."""
    track: SpotifyTrack
    played_at: str


class RecentlyPlayedResponse(BaseModel):
    """Response for recently played endpoint."""
    items: List[PlayHistoryItem]
    total: int
