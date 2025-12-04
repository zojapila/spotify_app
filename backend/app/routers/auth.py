"""Authentication router for Spotify OAuth."""

import secrets
from datetime import datetime, timedelta
from urllib.parse import urlencode
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import get_settings
from app.schemas.auth import TokenResponse
from app.database import get_db
from app.models.user_token import UserToken

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
    db: AsyncSession = Depends(get_db),
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
    
    # Get user profile to store with tokens
    async with httpx.AsyncClient() as client:
        profile_response = await client.get(
            f"{settings.spotify_api_base_url}/me",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        
        user_profile = profile_response.json() if profile_response.status_code == 200 else {}
    
    # Save or update user token in database for background tracking
    user_id = user_profile.get("id", "unknown")
    
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    existing_token = result.scalar_one_or_none()
    
    token_expires_at = datetime.utcnow() + timedelta(seconds=tokens["expires_in"])
    
    if existing_token:
        # Update existing token
        existing_token.access_token = tokens["access_token"]
        existing_token.refresh_token = tokens.get("refresh_token", existing_token.refresh_token)
        existing_token.token_expires_at = token_expires_at
        existing_token.display_name = user_profile.get("display_name")
        existing_token.email = user_profile.get("email")
    else:
        # Create new token
        new_token = UserToken(
            user_id=user_id,
            display_name=user_profile.get("display_name"),
            email=user_profile.get("email"),
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token", ""),
            token_expires_at=token_expires_at,
            tracking_enabled=True,
        )
        db.add(new_token)
    
    await db.commit()
    
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
