"""Pydantic schemas for request/response validation."""

from app.schemas.spotify import (
    SpotifyUser,
    SpotifyArtist,
    SpotifyTrack,
    SpotifyAlbum,
    TopArtistsResponse,
    TopTracksResponse,
    TopAlbumsResponse,
    RecentlyPlayedResponse,
)
from app.schemas.tracking import (
    RecordPlayRequest,
    RecordPlayResponse,
    TrackingStats,
    TrackingHistory,
    TrackPlayCount,
    ArtistPlayCount,
)
from app.schemas.auth import (
    TokenResponse,
    AuthCallbackResponse,
)

__all__ = [
    # Spotify
    "SpotifyUser",
    "SpotifyArtist", 
    "SpotifyTrack",
    "SpotifyAlbum",
    "TopArtistsResponse",
    "TopTracksResponse",
    "TopAlbumsResponse",
    "RecentlyPlayedResponse",
    # Tracking
    "RecordPlayRequest",
    "RecordPlayResponse",
    "TrackingStats",
    "TrackingHistory",
    "TrackPlayCount",
    "ArtistPlayCount",
    # Auth
    "TokenResponse",
    "AuthCallbackResponse",
]
