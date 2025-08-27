import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.juhe_geolocation_service import JuheGeolocationService


class TestJuheGeolocationService:
    """Test suite for JuheGeolocationService"""

    @pytest.fixture
    def service(self):
        """Create a service instance for testing"""
        return JuheGeolocationService()

    @pytest.fixture
    def mock_response(self):
        """Mock successful API response"""
        return {
            "error_code": 0,
            "reason": "success",
            "result": {
                "location": "116.397128,39.916527",
                "formatted_address": "北京市朝阳区",
                "country": "中国",
                "province": "北京市",
                "city": "北京市",
                "district": "朝阳区"
            }
        }

    @pytest.mark.asyncio
    async def test_geocode_address_success(self, service, mock_response):
        """Test successful address geocoding"""
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.status_code = 200

            result = await service.geocode_address("北京市朝阳区")

            assert result is not None
            assert result["error_code"] == 0
            assert "location" in result["result"]
            mock_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_geocode_address_failure(self, service):
        """Test address geocoding with API error"""
        error_response = {"error_code": 10001, "reason": "Invalid API key"}
        
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.json.return_value = error_response
            mock_get.return_value.status_code = 200

            result = await service.geocode_address("Invalid Address")

            assert result is not None
            assert result["error_code"] == 10001
            assert "Invalid API key" in result["reason"]

    @pytest.mark.asyncio
    async def test_reverse_geocode_success(self, service, mock_response):
        """Test successful reverse geocoding"""
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.status_code = 200

            result = await service.reverse_geocode(116.397128, 39.916527)

            assert result is not None
            assert result["error_code"] == 0
            assert "formatted_address" in result["result"]

    @pytest.mark.asyncio
    async def test_calculate_distance_haversine(self, service):
        """Test distance calculation using Haversine formula"""
        # Test coordinates for New York and Los Angeles
        lat1, lng1 = 40.7128, -74.0060  # New York
        lat2, lng2 = 34.0522, -118.2437  # Los Angeles

        distance = service.calculate_distance_haversine(lat1, lng1, lat2, lng2)
        
        # Distance should be approximately 3935 km
        assert 3900 <= distance <= 4000
        assert isinstance(distance, float)

    @pytest.mark.asyncio
    async def test_get_route_directions_success(self, service):
        """Test successful route directions"""
        route_response = {
            "error_code": 0,
            "reason": "success",
            "result": {
                "distance": "1000",
                "duration": "600",
                "steps": [
                    {"instruction": "Start at point A", "distance": "100"},
                    {"instruction": "Turn right", "distance": "200"}
                ]
            }
        }

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.json.return_value = route_response
            mock_get.return_value.status_code = 200

            result = await service.get_route_directions(
                origin_lat=40.7128, origin_lng=-74.0060,
                dest_lat=40.7589, dest_lng=-73.9851
            )

            assert result is not None
            assert result["error_code"] == 0
            assert "distance" in result["result"]

    @pytest.mark.asyncio
    async def test_get_nearby_places_success(self, service):
        """Test successful nearby places search"""
        places_response = {
            "error_code": 0,
            "reason": "success",
            "result": {
                "total": 10,
                "data": [
                    {"name": "Restaurant A", "distance": "100m"},
                    {"name": "Restaurant B", "distance": "200m"}
                ]
            }
        }

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.json.return_value = places_response
            mock_get.return_value.status_code = 200

            result = await service.get_nearby_places(
                lat=40.7128, lng=-74.0060, 
                radius=1000, types="restaurant"
            )

            assert result is not None
            assert result["error_code"] == 0
            assert "data" in result["result"]
            assert len(result["result"]["data"]) == 2

    def test_validate_coordinates_valid(self, service):
        """Test coordinate validation with valid coordinates"""
        assert service.validate_coordinates(40.7128, -74.0060) is True
        assert service.validate_coordinates(0, 0) is True
        assert service.validate_coordinates(-90, 180) is True

    def test_validate_coordinates_invalid(self, service):
        """Test coordinate validation with invalid coordinates"""
        assert service.validate_coordinates(91, 0) is False  # Latitude too high
        assert service.validate_coordinates(-91, 0) is False  # Latitude too low
        assert service.validate_coordinates(0, 181) is False  # Longitude too high
        assert service.validate_coordinates(0, -181) is False  # Longitude too low
        assert service.validate_coordinates("invalid", 0) is False  # Non-numeric

    @pytest.mark.asyncio
    async def test_get_location_info_success(self, service, mock_response):
        """Test successful location info retrieval"""
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.status_code = 200

            result = await service.get_location_info(116.397128, 39.916527)

            assert result is not None
            assert result["error_code"] == 0
            assert "formatted_address" in result["result"]

    @pytest.mark.asyncio
    async def test_optimize_route_simple(self, service):
        """Test simple route optimization"""
        points = [
            (40.7128, -74.0060),  # New York
            (34.0522, -118.2437),  # Los Angeles
            (41.8781, -87.6298),   # Chicago
        ]

        optimized_route = service.optimize_route_simple(points)
        
        assert len(optimized_route) == len(points)
        assert all(isinstance(point, tuple) for point in optimized_route)
        assert len(optimized_route[0]) == 2  # Each point should have lat, lng

    @pytest.mark.asyncio
    async def test_api_timeout_handling(self, service):
        """Test API timeout handling"""
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = Exception("Timeout")

            result = await service.geocode_address("Test Address")

            assert result is not None
            assert result["error_code"] == -1
            assert "error" in result

    @pytest.mark.asyncio
    async def test_network_error_handling(self, service):
        """Test network error handling"""
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = ConnectionError("Network error")

            result = await service.reverse_geocode(40.7128, -74.0060)

            assert result is not None
            assert result["error_code"] == -1
            assert "error" in result

    def test_coordinate_precision(self, service):
        """Test coordinate precision handling"""
        # Test with high precision coordinates
        lat, lng = 40.7128123456789, -74.0060123456789
        
        # Should handle high precision without issues
        assert service.validate_coordinates(lat, lng) is True

    @pytest.mark.asyncio
    async def test_empty_address_handling(self, service):
        """Test handling of empty address"""
        result = await service.geocode_address("")
        
        assert result is not None
        assert result["error_code"] == -1
        assert "error" in result

    @pytest.mark.asyncio
    async def test_none_coordinates_handling(self, service):
        """Test handling of None coordinates"""
        result = await service.reverse_geocode(None, None)
        
        assert result is not None
        assert result["error_code"] == -1
        assert "error" in result


if __name__ == "__main__":
    pytest.main([__file__])
