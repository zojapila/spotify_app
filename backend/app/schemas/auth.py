"""Authentication schemas."""

from pydantic import BaseModel
from typing import Optional


class TokenResponse(BaseModel):
    """Response with access token."""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class AuthCallbackResponse(BaseModel):
    """Response after successful OAuth callback."""
    access_token: str
    refresh_token: str
    expires_in: int
    user_id: str
    display_name: Optional[str] = None
