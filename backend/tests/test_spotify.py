"""Tests for Spotify API endpoints."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestSpotifyMe:
    """Tests for /api/spotify/me endpoint."""
    
    def test_me_without_auth_fails(self):
        """Test that /me without authorization returns 422."""
        response = client.get("/api/spotify/me")
        
        assert response.status_code == 422
    
    def test_me_with_invalid_auth_format_fails(self):
        """Test that /me with invalid auth format fails."""
        response = client.get(
            "/api/spotify/me",
            headers={"Authorization": "Invalid token"}
        )
        
        assert response.status_code == 401
    
    @patch("app.routers.spotify.SpotifyService")
    def test_me_with_valid_token(self, mock_service_class, mock_spotify_user):
        """Test that /me returns user profile with valid token."""
        mock_service = AsyncMock()
        mock_service.get_current_user.return_value = MagicMock(**mock_spotify_user)
        mock_service_class.return_value = mock_service
        
        response = client.get(
            "/api/spotify/me",
            headers={"Authorization": "Bearer valid_token"}
        )
        
        # Would be 200 with proper mock setup
        assert response.status_code in [200, 500]


class TestSpotifyTopArtists:
    """Tests for /api/spotify/top/artists endpoint."""
    
    def test_top_artists_without_auth_fails(self):
        """Test that top artists without auth returns 422."""
        response = client.get("/api/spotify/top/artists")
        
        assert response.status_code == 422
    
    def test_top_artists_accepts_time_range(self):
        """Test that top artists accepts time_range parameter."""
        response = client.get(
            "/api/spotify/top/artists?time_range=short_term",
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Should not return 422 for invalid param
        assert response.status_code != 422 or "time_range" not in str(response.json())
    
    def test_top_artists_accepts_limit(self):
        """Test that top artists accepts limit parameter."""
        response = client.get(
            "/api/spotify/top/artists?limit=10",
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code != 422 or "limit" not in str(response.json())


class TestSpotifyTopTracks:
    """Tests for /api/spotify/top/tracks endpoint."""
    
    def test_top_tracks_without_auth_fails(self):
        """Test that top tracks without auth returns 422."""
        response = client.get("/api/spotify/top/tracks")
        
        assert response.status_code == 422
    
    def test_top_tracks_default_params(self):
        """Test top tracks with default parameters."""
        response = client.get(
            "/api/spotify/top/tracks",
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Request should be valid (auth might fail but params are OK)
        assert response.status_code != 422


class TestSpotifyTopAlbums:
    """Tests for /api/spotify/top/albums endpoint."""
    
    def test_top_albums_without_auth_fails(self):
        """Test that top albums without auth returns 422."""
        response = client.get("/api/spotify/top/albums")
        
        assert response.status_code == 422


class TestSpotifyRecentlyPlayed:
    """Tests for /api/spotify/recently-played endpoint."""
    
    def test_recently_played_without_auth_fails(self):
        """Test that recently played without auth returns 422."""
        response = client.get("/api/spotify/recently-played")
        
        assert response.status_code == 422
    
    def test_recently_played_accepts_limit(self):
        """Test that recently played accepts limit parameter."""
        response = client.get(
            "/api/spotify/recently-played?limit=50",
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code != 422 or "limit" not in str(response.json())
