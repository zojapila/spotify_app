"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import create_tables
from app.routers import auth_router, spotify_router, tracking_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await create_tables()
    print("🚀 Spotify Stats API started!")
    print(f"📊 API docs: http://localhost:8000/docs")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title="Spotify Stats API",
    description="API for viewing Spotify statistics and tracking listening history",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(spotify_router)
app.include_router(tracking_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Spotify Stats API",
        "docs": "/docs",
        "health": "ok",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
