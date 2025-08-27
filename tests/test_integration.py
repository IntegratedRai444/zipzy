import pytest
import asyncio
import json
import time
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import websockets
import httpx
from app.main_simple import app
from app.services.juhe_geolocation_service import JuheGeolocationService
from app.services.cache_service import CacheService
from app.security.location_privacy import LocationPrivacyService
from app.middleware.rate_limiter import RateLimiter


class TestGeolocationIntegration:
    """Integration tests for the complete geolocation system"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)

    @pytest.fixture
    def geolocation_service(self):
        """Create geolocation service instance"""
        return JuheGeolocationService()

    @pytest.fixture
    def cache_service(self):
        """Create cache service instance"""
        return CacheService()

    @pytest.fixture
    def privacy_service(self):
        """Create privacy service instance"""
        return LocationPrivacyService()

    @pytest.fixture
    def rate_limiter(self):
        """Create rate limiter instance"""
        return RateLimiter()

    @pytest.mark.asyncio
    async def test_complete_geocoding_flow(self, client, geolocation_service, cache_service):
        """Test complete geocoding flow with caching"""
        # Mock the geolocation service response
        mock_response = {
            "error_code": 0,
            "result": {
                "location": "40.7128,-74.0060",
                "formatted_address": "New York, NY"
            }
        }

        with patch.object(geolocation_service, 'geocode_address', return_value=mock_response):
            # Test geocoding endpoint
            response = client.post("/api/geolocation/geocode", json={"address": "New York, NY"})
            assert response.status_code == 200
            data = response.json()
            assert data["error_code"] == 0
            assert "location" in data["result"]

            # Test caching
            cached_result = await cache_service.get("geocoding", "New York, NY")
            assert cached_result is not None
            assert cached_result["error_code"] == 0

    @pytest.mark.asyncio
    async def test_complete_reverse_geocoding_flow(self, client, geolocation_service, cache_service):
        """Test complete reverse geocoding flow with caching"""
        mock_response = {
            "error_code": 0,
            "result": {
                "formatted_address": "New York, NY",
                "city": "New York"
            }
        }

        with patch.object(geolocation_service, 'reverse_geocode', return_value=mock_response):
            # Test reverse geocoding endpoint
            response = client.post("/api/geolocation/reverse-geocode", 
                                 json={"lat": 40.7128, "lng": -74.0060})
            assert response.status_code == 200
            data = response.json()
            assert data["error_code"] == 0
            assert "formatted_address" in data["result"]

            # Test caching
            cached_result = await cache_service.get("reverse_geocoding", 40.7128, -74.0060)
            assert cached_result is not None
            assert cached_result["error_code"] == 0

    @pytest.mark.asyncio
    async def test_complete_route_calculation_flow(self, client, geolocation_service, cache_service):
        """Test complete route calculation flow with caching"""
        mock_response = {
            "error_code": 0,
            "result": {
                "distance": "1000",
                "duration": "600",
                "steps": [{"instruction": "Start", "distance": "100"}]
            }
        }

        with patch.object(geolocation_service, 'get_route_directions', return_value=mock_response):
            # Test route calculation endpoint
            response = client.post("/api/geolocation/route", json={
                "origin_lat": 40.7128,
                "origin_lng": -74.0060,
                "dest_lat": 40.7589,
                "dest_lng": -73.9851
            })
            assert response.status_code == 200
            data = response.json()
            assert data["error_code"] == 0
            assert "distance" in data["result"]

            # Test caching
            cached_result = await cache_service.get("route_calculation", 
                                                  40.7128, -74.0060, 40.7589, -73.9851)
            assert cached_result is not None
            assert cached_result["error_code"] == 0

    @pytest.mark.asyncio
    async def test_complete_nearby_places_flow(self, client, geolocation_service, cache_service):
        """Test complete nearby places flow with caching"""
        mock_response = {
            "error_code": 0,
            "result": {
                "total": 5,
                "data": [
                    {"name": "Restaurant A", "distance": "100m"},
                    {"name": "Restaurant B", "distance": "200m"}
                ]
            }
        }

        with patch.object(geolocation_service, 'get_nearby_places', return_value=mock_response):
            # Test nearby places endpoint
            response = client.post("/api/geolocation/nearby-places", json={
                "lat": 40.7128,
                "lng": -74.0060,
                "radius": 1000,
                "types": "restaurant"
            })
            assert response.status_code == 200
            data = response.json()
            assert data["error_code"] == 0
            assert "data" in data["result"]

            # Test caching
            cached_result = await cache_service.get("nearby_places", 
                                                  40.7128, -74.0060, 1000, "restaurant")
            assert cached_result is not None
            assert cached_result["error_code"] == 0

    @pytest.mark.asyncio
    async def test_privacy_integration(self, client, privacy_service):
        """Test privacy service integration"""
        # Test location anonymization
        original_lat, original_lng = 40.7128, -74.0060
        anon_lat, anon_lng = privacy_service.anonymize_location(original_lat, original_lng, 100)
        
        # Anonymized coordinates should be different but close
        assert abs(anon_lat - original_lat) < 0.01
        assert abs(anon_lng - original_lng) < 0.01
        assert anon_lat != original_lat or anon_lng != original_lng

        # Test location encryption
        location_data = {
            "lat": original_lat,
            "lng": original_lng,
            "timestamp": "2024-01-01T12:00:00Z"
        }
        encrypted_data = privacy_service.encrypt_location_data(location_data)
        decrypted_data = privacy_service.decrypt_location_data(encrypted_data)
        
        assert decrypted_data["lat"] == location_data["lat"]
        assert decrypted_data["lng"] == location_data["lng"]

        # Test GDPR rights
        gdpr_response = privacy_service.implement_gdpr_rights("user123", "access")
        assert gdpr_response["right"] == "access"
        assert gdpr_response["user_id"] == "user123"

    @pytest.mark.asyncio
    async def test_rate_limiting_integration(self, client, rate_limiter):
        """Test rate limiting integration"""
        # Test rate limit checking
        client_id = "test_client"
        allowed, rate_limit_info = await rate_limiter.check_rate_limit(client_id, "geolocation")
        assert allowed is True

        # Test multiple requests to trigger rate limiting
        for i in range(100):  # Exceed the limit
            allowed, rate_limit_info = await rate_limiter.check_rate_limit(client_id, "geolocation")
            if not allowed:
                break
        
        # Should eventually hit rate limit
        assert allowed is False
        assert "limit_exceeded" in rate_limit_info

        # Test rate limit info
        info = await rate_limiter.get_rate_limit_info(client_id, "geolocation")
        assert "current_usage" in info
        assert "limits" in info

    @pytest.mark.asyncio
    async def test_cache_integration(self, cache_service):
        """Test cache service integration"""
        # Test setting and getting cache
        test_data = {"test": "data", "number": 123}
        success = await cache_service.set("test_cache", test_data, "key1", "key2")
        assert success is True

        cached_data = await cache_service.get("test_cache", "key1", "key2")
        assert cached_data == test_data

        # Test cache deletion
        success = await cache_service.delete("test_cache", "key1", "key2")
        assert success is True

        cached_data = await cache_service.get("test_cache", "key1", "key2")
        assert cached_data is None

        # Test cache stats
        stats = await cache_service.get_cache_stats()
        assert "cache_type" in stats
        assert "cache_config" in stats

    @pytest.mark.asyncio
    async def test_error_handling_integration(self, client):
        """Test error handling integration"""
        # Test invalid coordinates
        response = client.post("/api/geolocation/reverse-geocode", 
                             json={"lat": 200.0, "lng": -74.0060})  # Invalid latitude
        assert response.status_code == 400

        # Test missing required fields
        response = client.post("/api/geolocation/geocode", json={})
        assert response.status_code == 422

        # Test invalid data types
        response = client.post("/api/geolocation/reverse-geocode", 
                             json={"lat": "invalid", "lng": -74.0060})
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_coordinate_validation_integration(self, geolocation_service):
        """Test coordinate validation integration"""
        # Test valid coordinates
        assert geolocation_service.validate_coordinates(40.7128, -74.0060) is True
        assert geolocation_service.validate_coordinates(0, 0) is True
        assert geolocation_service.validate_coordinates(-90, 180) is True

        # Test invalid coordinates
        assert geolocation_service.validate_coordinates(91, 0) is False
        assert geolocation_service.validate_coordinates(-91, 0) is False
        assert geolocation_service.validate_coordinates(0, 181) is False
        assert geolocation_service.validate_coordinates(0, -181) is False

    @pytest.mark.asyncio
    async def test_distance_calculation_integration(self, geolocation_service):
        """Test distance calculation integration"""
        # Test distance calculation
        lat1, lng1 = 40.7128, -74.0060  # New York
        lat2, lng2 = 34.0522, -118.2437  # Los Angeles

        distance = geolocation_service.calculate_distance_haversine(lat1, lng1, lat2, lng2)
        assert 3900 <= distance <= 4000  # Should be approximately 3935 km

        # Test same location
        distance_same = geolocation_service.calculate_distance_haversine(lat1, lng1, lat1, lng1)
        assert distance_same == 0

    @pytest.mark.asyncio
    async def test_route_optimization_integration(self, geolocation_service):
        """Test route optimization integration"""
        # Test route optimization
        points = [
            (40.7128, -74.0060),  # New York
            (34.0522, -118.2437),  # Los Angeles
            (41.8781, -87.6298),   # Chicago
        ]

        optimized_route = geolocation_service.optimize_route_simple(points)
        assert len(optimized_route) == len(points)
        assert all(isinstance(point, tuple) for point in optimized_route)
        assert len(optimized_route[0]) == 2

    @pytest.mark.asyncio
    async def test_api_proxy_integration(self):
        """Test API proxy integration"""
        # This would test the Next.js API proxy routes
        # For now, we'll test the backend endpoints directly
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            # Test health endpoint
            response = await client.get("/api/geolocation/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_concurrent_requests_integration(self, client):
        """Test concurrent requests handling"""
        # Test multiple concurrent requests
        async def make_request():
            async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/api/geolocation/health")
                return response.status_code

        # Make multiple concurrent requests
        tasks = [make_request() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # All requests should succeed
        assert all(status == 200 for status in results)

    @pytest.mark.asyncio
    async def test_performance_integration(self, client, cache_service):
        """Test performance with caching"""
        # Test response time without cache
        start_time = time.time()
        response = client.get("/api/geolocation/health")
        first_request_time = time.time() - start_time

        # Test response time with cache
        start_time = time.time()
        response = client.get("/api/geolocation/health")
        second_request_time = time.time() - start_time

        # Second request should be faster (cached)
        assert second_request_time <= first_request_time

    @pytest.mark.asyncio
    async def test_security_integration(self, privacy_service):
        """Test security features integration"""
        # Test location hashing
        lat, lng = 40.7128, -74.0060
        user_id = "user123"
        
        location_hash, salt = privacy_service.create_location_hash(lat, lng, user_id)
        assert len(location_hash) == 64  # SHA-256 hash length
        assert len(salt) == 32  # 16 bytes hex encoded

        # Test anomaly detection
        previous_locations = [
            {"lat": 40.7128, "lng": -74.0060, "timestamp": "2024-01-01T12:00:00Z"},
            {"lat": 40.7129, "lng": -74.0061, "timestamp": "2024-01-01T12:01:00Z"}
        ]
        
        anomaly_result = privacy_service.check_location_anomaly(lat, lng, user_id, previous_locations)
        assert "anomaly_detected" in anomaly_result

    @pytest.mark.asyncio
    async def test_data_retention_integration(self, privacy_service):
        """Test data retention policy integration"""
        # Test data retention policy
        location_records = [
            {"lat": 40.7128, "lng": -74.0060, "timestamp": "2024-01-01T12:00:00Z"},
            {"lat": 40.7129, "lng": -74.0061, "timestamp": "2023-01-01T12:00:00Z"},  # Old record
        ]

        filtered_records = privacy_service.apply_data_retention_policy(location_records)
        assert len(filtered_records) <= len(location_records)

        # Test privacy report
        privacy_report = privacy_service.create_privacy_report("user123", location_records)
        assert privacy_report["user_id"] == "user123"
        assert "total_records" in privacy_report
        assert "retention_policy_records" in privacy_report

    @pytest.mark.asyncio
    async def test_websocket_integration_simulation(self):
        """Simulate WebSocket integration testing"""
        # This would test WebSocket connections in a real environment
        # For now, we'll test the WebSocket manager logic
        
        from app.api.geolocation import LocationWebSocketManager
        
        manager = LocationWebSocketManager()
        
        # Test connection management
        mock_websocket = MagicMock()
        user_id = "user123"
        
        # Test connection
        await manager.connect(mock_websocket, user_id)
        assert user_id in manager.active_connections
        assert len(manager.active_connections[user_id]) == 1

        # Test disconnection
        manager.disconnect(mock_websocket, user_id)
        assert user_id not in manager.active_connections

    @pytest.mark.asyncio
    async def test_complete_workflow_integration(self, client, geolocation_service, cache_service, privacy_service):
        """Test complete workflow integration"""
        # 1. User requests geocoding
        mock_geocode_response = {
            "error_code": 0,
            "result": {"location": "40.7128,-74.0060", "formatted_address": "New York, NY"}
        }

        with patch.object(geolocation_service, 'geocode_address', return_value=mock_geocode_response):
            response = client.post("/api/geolocation/geocode", json={"address": "New York, NY"})
            assert response.status_code == 200

        # 2. User requests nearby restaurants
        mock_restaurants_response = {
            "error_code": 0,
            "result": {
                "total": 3,
                "data": [
                    {"name": "Restaurant A", "distance": "100m"},
                    {"name": "Restaurant B", "distance": "200m"}
                ]
            }
        }

        with patch.object(geolocation_service, 'get_nearby_places', return_value=mock_restaurants_response):
            response = client.post("/api/geolocation/nearby-restaurants", json={
                "lat": 40.7128, "lng": -74.0060, "radius": 1000
            })
            assert response.status_code == 200

        # 3. User requests route calculation
        mock_route_response = {
            "error_code": 0,
            "result": {"distance": "500", "duration": "300", "steps": []}
        }

        with patch.object(geolocation_service, 'get_route_directions', return_value=mock_route_response):
            response = client.post("/api/geolocation/route", json={
                "origin_lat": 40.7128, "origin_lng": -74.0060,
                "dest_lat": 40.7589, "dest_lng": -73.9851
            })
            assert response.status_code == 200

        # 4. Test privacy features
        location_data = {"lat": 40.7128, "lng": -74.0060, "user_id": "user123"}
        encrypted_data = privacy_service.encrypt_location_data(location_data)
        assert encrypted_data is not None

        # 5. Test caching
        cached_data = await cache_service.get("geocoding", "New York, NY")
        assert cached_data is not None

        # 6. Test rate limiting
        from app.middleware.rate_limiter import rate_limiter
        allowed, _ = await rate_limiter.check_rate_limit("test_client", "geolocation")
        assert allowed is True


if __name__ == "__main__":
    pytest.main([__file__])
