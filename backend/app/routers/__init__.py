"""API routers."""

from app.routers.auth import router as auth_router
from app.routers.spotify import router as spotify_router
from app.routers.tracking import router as tracking_router

__all__ = ["auth_router", "spotify_router", "tracking_router"]
