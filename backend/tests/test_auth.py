"""Tests for authentication endpoints."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestAuthLogin:
    """Tests for /api/auth/login endpoint."""
    
    def test_login_redirects_to_spotify(self):
        """Test that login redirects to Spotify authorization page."""
        response = client.get("/api/auth/login", follow_redirects=False)
        
        assert response.status_code == 307
        assert "accounts.spotify.com/authorize" in response.headers["location"]
    
    def test_login_includes_required_params(self):
        """Test that login URL includes all required OAuth parameters."""
        response = client.get("/api/auth/login", follow_redirects=False)
        
        location = response.headers["location"]
        assert "client_id=" in location
        assert "response_type=code" in location
        assert "redirect_uri=" in location
        assert "scope=" in location
        assert "state=" in location


class TestAuthCallback:
    """Tests for /api/auth/callback endpoint."""
    
    def test_callback_without_code_fails(self):
        """Test that callback without code returns error."""
        response = client.get("/api/auth/callback?state=test")
        
        assert response.status_code == 400
    
    def test_callback_with_error_redirects(self):
        """Test that callback with error redirects to frontend."""
        response = client.get(
            "/api/auth/callback?error=access_denied",
            follow_redirects=False
        )
        
        assert response.status_code == 307
        assert "error=access_denied" in response.headers["location"]
    
    def test_callback_with_invalid_state_fails(self):
        """Test that callback with invalid state returns error."""
        response = client.get("/api/auth/callback?code=test&state=invalid")
        
        assert response.status_code == 400
        assert "Invalid state" in response.json()["detail"]


class TestAuthRefresh:
    """Tests for /api/auth/refresh endpoint."""
    
    @patch("app.routers.auth.httpx.AsyncClient")
    def test_refresh_with_valid_token(self, mock_client):
        """Test token refresh with valid refresh token."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "user-read-private",
        }
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_client.return_value = mock_client_instance
        
        response = client.post(
            "/api/auth/refresh",
            params={"refresh_token": "valid_refresh_token"}
        )
        
        assert response.status_code == 200
        assert "access_token" in response.json()


class TestAuthLogout:
    """Tests for /api/auth/logout endpoint."""
    
    def test_logout_returns_success(self):
        """Test that logout returns success message."""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"
