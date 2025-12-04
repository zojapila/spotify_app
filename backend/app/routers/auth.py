"""Authentication router for Spotify OAuth."""

import secrets
from urllib.parse import urlencode
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
import httpx

from app.config import get_settings
from app.schemas.auth import TokenResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = get_settings()

# In-memory state storage (use Redis in production)
oauth_states: dict[str, bool] = {}


@router.get("/login")
async def login():
    """Redirect to Spotify authorization page."""
    state = secrets.token_urlsafe(16)
    oauth_states[state] = True
    
    params = {
        "client_id": settings.spotify_client_id,
        "response_type": "code",
        "redirect_uri": settings.spotify_redirect_uri,
        "scope": settings.spotify_scopes,
        "state": state,
        "show_dialog": "true",  # Always show dialog for testing
    }
    
    auth_url = f"{settings.spotify_auth_url}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def callback(
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None),
):
    """Handle Spotify OAuth callback."""
    if error:
        return RedirectResponse(
            url=f"{settings.frontend_url}/login?error={error}"
        )
    
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state")
    
    # Verify state (prevent CSRF)
    if state not in oauth_states:
        raise HTTPException(status_code=400, detail="Invalid state")
    
    del oauth_states[state]
    
    # Exchange code for tokens
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.spotify_token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.spotify_redirect_uri,
                "client_id": settings.spotify_client_id,
                "client_secret": settings.spotify_client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to get tokens: {response.text}"
            )
        
        tokens = response.json()
    
    # Redirect to frontend with tokens in URL params
    # In production, use secure HTTP-only cookies instead
    params = urlencode({
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token", ""),
        "expires_in": tokens["expires_in"],
    })
    
    return RedirectResponse(url=f"{settings.frontend_url}/dashboard?{params}")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.spotify_token_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.spotify_client_id,
                "client_secret": settings.spotify_client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=401,
                detail="Failed to refresh token"
            )
        
        tokens = response.json()
        
        return TokenResponse(
            access_token=tokens["access_token"],
            token_type="Bearer",
            expires_in=tokens["expires_in"],
            refresh_token=tokens.get("refresh_token"),
            scope=tokens.get("scope"),
        )


@router.post("/logout")
async def logout():
    """Logout user (client should clear tokens)."""
    return {"message": "Successfully logged out"}
