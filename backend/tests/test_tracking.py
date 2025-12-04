"""Tests for tracking service and endpoints."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, AsyncMock

from app.services.tracking_service import TrackingService
from app.schemas.tracking import RecordPlayRequest
from app.models.listening_session import ListeningSession


class TestTrackingService:
    """Tests for TrackingService."""
    
    @pytest.mark.asyncio
    async def test_record_play_creates_session(self, test_db):
        """Test that record_play creates a new listening session."""
        service = TrackingService(test_db, "user123")
        
        request = RecordPlayRequest(
            track_id="track123",
            track_name="Test Track",
            artist_name="Test Artist",
            album_name="Test Album",
            duration_ms=180000,
        )
        
        response = await service.record_play(request)
        
        assert response.recorded is True
        assert response.id is not None
        assert "recorded" in response.message.lower()
    
    @pytest.mark.asyncio
    async def test_record_play_detects_duplicates(self, test_db):
        """Test that record_play detects duplicate plays within 3 minutes."""
        service = TrackingService(test_db, "user123")
        
        request = RecordPlayRequest(
            track_id="track123",
            track_name="Test Track",
            artist_name="Test Artist",
            album_name="Test Album",
            duration_ms=180000,
        )
        
        # First play
        response1 = await service.record_play(request)
        assert response1.recorded is True
        
        # Duplicate play (within 3 minutes)
        response2 = await service.record_play(request)
        assert response2.recorded is False
        assert "duplicate" in response2.message.lower()
    
    @pytest.mark.asyncio
    async def test_get_stats_empty(self, test_db):
        """Test get_stats with no listening history."""
        service = TrackingService(test_db, "user123")
        
        stats = await service.get_stats(days=30)
        
        assert stats.total_plays == 0
        assert stats.total_time_ms == 0
        assert stats.unique_tracks == 0
        assert len(stats.top_tracks) == 0
    
    @pytest.mark.asyncio
    async def test_get_stats_with_data(self, test_db):
        """Test get_stats with listening history."""
        service = TrackingService(test_db, "user123")
        
        # Add some listening sessions
        for i in range(5):
            request = RecordPlayRequest(
                track_id=f"track{i}",
                track_name=f"Track {i}",
                artist_name="Test Artist",
                album_name="Test Album",
                duration_ms=180000,
            )
            # Create session directly to avoid duplicate detection
            session = ListeningSession(
                user_id="user123",
                track_id=f"track{i}",
                track_name=f"Track {i}",
                artist_name="Test Artist",
                album_name="Test Album",
                duration_ms=180000,
                played_at=datetime.utcnow() - timedelta(minutes=i * 10),
            )
            test_db.add(session)
        
        await test_db.commit()
        
        stats = await service.get_stats(days=30)
        
        assert stats.total_plays == 5
        assert stats.total_time_ms == 5 * 180000
        assert stats.unique_tracks == 5
        assert stats.unique_artists == 1
    
    @pytest.mark.asyncio
    async def test_get_history(self, test_db):
        """Test get_history returns sessions in correct order."""
        service = TrackingService(test_db, "user123")
        
        # Add sessions
        for i in range(3):
            session = ListeningSession(
                user_id="user123",
                track_id=f"track{i}",
                track_name=f"Track {i}",
                artist_name="Test Artist",
                album_name="Test Album",
                duration_ms=180000,
                played_at=datetime.utcnow() - timedelta(hours=i),
            )
            test_db.add(session)
        
        await test_db.commit()
        
        history = await service.get_history(days=30, limit=10)
        
        assert history.total == 3
        assert len(history.items) == 3
        # Most recent first
        assert history.items[0].track_name == "Track 0"
    
    def test_format_time_minutes(self):
        """Test time formatting for minutes."""
        result = TrackingService._format_time(300000)  # 5 minutes
        assert result == "5m"
    
    def test_format_time_hours(self):
        """Test time formatting for hours."""
        result = TrackingService._format_time(3900000)  # 1h 5m
        assert result == "1h 5m"


class TestTrackingEndpoints:
    """Tests for tracking API endpoints."""
    
    def test_record_without_auth_fails(self):
        """Test that record endpoint requires authentication."""
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        response = client.post(
            "/api/tracking/record",
            json={
                "track_id": "test",
                "track_name": "Test",
                "artist_name": "Test",
                "album_name": "Test",
                "duration_ms": 180000,
            }
        )
        
        assert response.status_code == 422  # Missing auth header
    
    def test_stats_without_auth_fails(self):
        """Test that stats endpoint requires authentication."""
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        response = client.get("/api/tracking/stats")
        
        assert response.status_code == 422
    
    def test_history_without_auth_fails(self):
        """Test that history endpoint requires authentication."""
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        response = client.get("/api/tracking/history")
        
        assert response.status_code == 422
