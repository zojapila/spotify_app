"""Test configuration and fixtures."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.database import Base


@pytest.fixture
def mock_spotify_user():
    """Mock Spotify user data."""
    return {
        "id": "test_user_123",
        "display_name": "Test User",
        "email": "test@example.com",
        "images": [{"url": "https://example.com/image.jpg", "height": 300, "width": 300}],
        "product": "premium",
        "followers": {"total": 42},
    }


@pytest.fixture
def mock_top_artists():
    """Mock top artists response."""
    return {
        "items": [
            {
                "id": "artist1",
                "name": "Arctic Monkeys",
                "genres": ["rock", "indie rock"],
                "popularity": 85,
                "images": [{"url": "https://example.com/artist1.jpg"}],
                "external_urls": {"spotify": "https://open.spotify.com/artist/artist1"},
            },
            {
                "id": "artist2",
                "name": "Tame Impala",
                "genres": ["psychedelic rock", "indie"],
                "popularity": 80,
                "images": [{"url": "https://example.com/artist2.jpg"}],
                "external_urls": {"spotify": "https://open.spotify.com/artist/artist2"},
            },
        ],
        "total": 50,
        "limit": 20,
        "offset": 0,
    }


@pytest.fixture
def mock_top_tracks():
    """Mock top tracks response."""
    return {
        "items": [
            {
                "id": "track1",
                "name": "Do I Wanna Know?",
                "duration_ms": 272000,
                "popularity": 88,
                "album": {
                    "id": "album1",
                    "name": "AM",
                    "images": [{"url": "https://example.com/album1.jpg"}],
                    "release_date": "2013-09-09",
                },
                "artists": [{"id": "artist1", "name": "Arctic Monkeys"}],
                "external_urls": {"spotify": "https://open.spotify.com/track/track1"},
            },
            {
                "id": "track2",
                "name": "The Less I Know The Better",
                "duration_ms": 216000,
                "popularity": 85,
                "album": {
                    "id": "album2",
                    "name": "Currents",
                    "images": [{"url": "https://example.com/album2.jpg"}],
                    "release_date": "2015-07-17",
                },
                "artists": [{"id": "artist2", "name": "Tame Impala"}],
                "external_urls": {"spotify": "https://open.spotify.com/track/track2"},
            },
        ],
        "total": 50,
        "limit": 20,
        "offset": 0,
    }


@pytest.fixture
def mock_recently_played():
    """Mock recently played response."""
    return {
        "items": [
            {
                "track": {
                    "id": "track1",
                    "name": "Do I Wanna Know?",
                    "duration_ms": 272000,
                    "album": {
                        "id": "album1",
                        "name": "AM",
                        "images": [{"url": "https://example.com/album1.jpg"}],
                    },
                    "artists": [{"id": "artist1", "name": "Arctic Monkeys"}],
                },
                "played_at": "2024-01-15T14:30:00Z",
            }
        ],
    }


@pytest.fixture
async def test_db():
    """Create test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest.fixture
def mock_access_token():
    """Mock access token."""
    return "mock_access_token_12345"
