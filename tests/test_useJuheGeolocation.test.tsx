import React from 'react';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useJuheGeolocation } from '../app/hooks/useJuheGeolocation';
import axios from 'axios';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock navigator.geolocation
const mockGeolocation = {
  getCurrentPosition: jest.fn(),
  watchPosition: jest.fn(),
  clearWatch: jest.fn(),
};

Object.defineProperty(global.navigator, 'geolocation', {
  value: mockGeolocation,
  writable: true,
});

// Mock WebSocket
global.WebSocket = jest.fn().mockImplementation(() => ({
  send: jest.fn(),
  close: jest.fn(),
  readyState: WebSocket.OPEN,
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
}));

describe('useJuheGeolocation', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockedAxios.post.mockResolvedValue({ data: { success: true } });
    mockedAxios.get.mockResolvedValue({ data: { success: true } });
  });

  it('should initialize with default state', () => {
    const { result } = renderHook(() => useJuheGeolocation());

    expect(result.current.location).toBeNull();
    expect(result.current.locationInfo).toBeNull();
    expect(result.current.error).toBeNull();
    expect(result.current.isLoading).toBe(false);
    expect(result.current.isTracking).toBe(false);
  });

  it('should start tracking location successfully', async () => {
    const mockPosition = {
      coords: {
        latitude: 40.7128,
        longitude: -74.0060,
        accuracy: 10,
      },
      timestamp: Date.now(),
    };

    mockGeolocation.watchPosition.mockImplementation((success) => {
      success(mockPosition);
      return 123; // watchId
    });

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      await result.current.startTracking();
    });

    expect(result.current.isTracking).toBe(true);
    expect(result.current.location).toEqual({
      lat: 40.7128,
      lng: -74.0060,
      accuracy: 10,
      timestamp: mockPosition.timestamp,
    });
  });

  it('should handle geolocation errors', async () => {
    const mockError = new Error('Geolocation permission denied');

    mockGeolocation.watchPosition.mockImplementation((success, error) => {
      error(mockError);
      return 123;
    });

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      await result.current.startTracking();
    });

    expect(result.current.error).toBe('Geolocation permission denied');
    expect(result.current.isTracking).toBe(false);
  });

  it('should stop tracking location', async () => {
    const { result } = renderHook(() => useJuheGeolocation());

    // Start tracking first
    mockGeolocation.watchPosition.mockReturnValue(123);
    await act(async () => {
      await result.current.startTracking();
    });

    // Stop tracking
    await act(async () => {
      await result.current.stopTracking();
    });

    expect(result.current.isTracking).toBe(false);
    expect(mockGeolocation.clearWatch).toHaveBeenCalledWith(123);
  });

  it('should geocode address successfully', async () => {
    const mockResponse = {
      data: {
        error_code: 0,
        result: {
          location: '40.7128,-74.0060',
          formatted_address: 'New York, NY',
        },
      },
    };

    mockedAxios.post.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      const response = await result.current.geocodeAddress('New York, NY');
      expect(response).toEqual(mockResponse.data);
    });

    expect(mockedAxios.post).toHaveBeenCalledWith(
      '/api/geolocation/geocode',
      { address: 'New York, NY' }
    );
  });

  it('should handle geocoding errors', async () => {
    const mockError = new Error('Network error');
    mockedAxios.post.mockRejectedValue(mockError);

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      const response = await result.current.geocodeAddress('Invalid Address');
      expect(response.error_code).toBe(-1);
      expect(response.error).toBe('Network error');
    });
  });

  it('should reverse geocode coordinates successfully', async () => {
    const mockResponse = {
      data: {
        error_code: 0,
        result: {
          formatted_address: 'New York, NY',
          city: 'New York',
        },
      },
    };

    mockedAxios.post.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      const response = await result.current.reverseGeocode(40.7128, -74.0060);
      expect(response).toEqual(mockResponse.data);
    });

    expect(mockedAxios.post).toHaveBeenCalledWith(
      '/api/geolocation/reverse-geocode',
      { lat: 40.7128, lng: -74.0060 }
    );
  });

  it('should get route directions successfully', async () => {
    const mockResponse = {
      data: {
        error_code: 0,
        result: {
          distance: '1000',
          duration: '600',
          steps: [{ instruction: 'Start', distance: '100' }],
        },
      },
    };

    mockedAxios.post.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      const response = await result.current.getRoute(
        40.7128, -74.0060, 40.7589, -73.9851
      );
      expect(response).toEqual(mockResponse.data);
    });

    expect(mockedAxios.post).toHaveBeenCalledWith(
      '/api/geolocation/route',
      {
        origin_lat: 40.7128,
        origin_lng: -74.0060,
        dest_lat: 40.7589,
        dest_lng: -73.9851,
      }
    );
  });

  it('should get nearby restaurants successfully', async () => {
    const mockResponse = {
      data: {
        error_code: 0,
        result: {
          total: 5,
          data: [
            { name: 'Restaurant A', distance: '100m' },
            { name: 'Restaurant B', distance: '200m' },
          ],
        },
      },
    };

    mockedAxios.post.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      const response = await result.current.getNearbyRestaurants(
        40.7128, -74.0060, 1000
      );
      expect(response).toEqual(mockResponse.data);
    });

    expect(mockedAxios.post).toHaveBeenCalledWith(
      '/api/geolocation/nearby-restaurants',
      { lat: 40.7128, lng: -74.0060, radius: 1000 }
    );
  });

  it('should calculate distance successfully', async () => {
    const mockResponse = {
      data: {
        distance: 1000.5,
        unit: 'km',
      },
    };

    mockedAxios.post.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      const response = await result.current.calculateDistance(
        40.7128, -74.0060, 40.7589, -73.9851
      );
      expect(response).toEqual(mockResponse.data);
    });

    expect(mockedAxios.post).toHaveBeenCalledWith(
      '/api/geolocation/distance',
      {
        lat1: 40.7128,
        lng1: -74.0060,
        lat2: 40.7589,
        lng2: -73.9851,
      }
    );
  });

  it('should connect to WebSocket successfully', async () => {
    const mockWebSocket = {
      send: jest.fn(),
      close: jest.fn(),
      readyState: WebSocket.OPEN,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    };

    (global.WebSocket as jest.Mock).mockImplementation(() => mockWebSocket);

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      await result.current.connectWebSocket('user123');
    });

    expect(global.WebSocket).toHaveBeenCalledWith(
      'ws://localhost:8000/api/geolocation/ws/location/user123'
    );
  });

  it('should send location updates via WebSocket', async () => {
    const mockWebSocket = {
      send: jest.fn(),
      close: jest.fn(),
      readyState: WebSocket.OPEN,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    };

    (global.WebSocket as jest.Mock).mockImplementation(() => mockWebSocket);

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      await result.current.sendLocationUpdate(40.7128, -74.0060);
    });

    expect(mockWebSocket.send).toHaveBeenCalledWith(
      JSON.stringify({
        lat: 40.7128,
        lng: -74.0060,
        timestamp: expect.any(Number),
      })
    );
  });

  it('should handle WebSocket connection errors', async () => {
    const mockError = new Error('WebSocket connection failed');
    (global.WebSocket as jest.Mock).mockImplementation(() => {
      throw mockError;
    });

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      await result.current.connectWebSocket('user123');
    });

    expect(result.current.error).toBe('WebSocket connection failed');
  });

  it('should update location state when tracking', async () => {
    const mockPosition = {
      coords: {
        latitude: 40.7128,
        longitude: -74.0060,
        accuracy: 10,
      },
      timestamp: Date.now(),
    };

    mockGeolocation.watchPosition.mockImplementation((success) => {
      success(mockPosition);
      return 123;
    });

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      await result.current.startTracking();
    });

    expect(result.current.location).toEqual({
      lat: 40.7128,
      lng: -74.0060,
      accuracy: 10,
      timestamp: mockPosition.timestamp,
    });
  });

  it('should handle API timeout errors', async () => {
    const timeoutError = new Error('Request timeout');
    timeoutError.name = 'TimeoutError';
    mockedAxios.post.mockRejectedValue(timeoutError);

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      const response = await result.current.geocodeAddress('Test Address');
      expect(response.error_code).toBe(-1);
      expect(response.error).toBe('Request timeout');
    });
  });

  it('should handle invalid coordinates', async () => {
    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      const response = await result.current.reverseGeocode(200, 200); // Invalid coordinates
      expect(response.error_code).toBe(-1);
      expect(response.error).toContain('Invalid coordinates');
    });
  });

  it('should cleanup WebSocket on unmount', () => {
    const mockWebSocket = {
      send: jest.fn(),
      close: jest.fn(),
      readyState: WebSocket.OPEN,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    };

    (global.WebSocket as jest.Mock).mockImplementation(() => mockWebSocket);

    const { result, unmount } = renderHook(() => useJuheGeolocation());

    // Connect WebSocket
    act(() => {
      result.current.connectWebSocket('user123');
    });

    // Unmount component
    unmount();

    expect(mockWebSocket.close).toHaveBeenCalled();
  });

  it('should handle geolocation permission denied', async () => {
    const permissionError = new Error('User denied geolocation');
    permissionError.name = 'GeolocationPositionError';
    (permissionError as any).code = 1;

    mockGeolocation.watchPosition.mockImplementation((success, error) => {
      error(permissionError);
      return 123;
    });

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      await result.current.startTracking();
    });

    expect(result.current.error).toBe('User denied geolocation');
    expect(result.current.isTracking).toBe(false);
  });

  it('should handle geolocation unavailable', async () => {
    const unavailableError = new Error('Geolocation unavailable');
    unavailableError.name = 'GeolocationPositionError';
    (unavailableError as any).code = 2;

    mockGeolocation.watchPosition.mockImplementation((success, error) => {
      error(unavailableError);
      return 123;
    });

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      await result.current.startTracking();
    });

    expect(result.current.error).toBe('Geolocation unavailable');
    expect(result.current.isTracking).toBe(false);
  });

  it('should handle geolocation timeout', async () => {
    const timeoutError = new Error('Geolocation timeout');
    timeoutError.name = 'GeolocationPositionError';
    (timeoutError as any).code = 3;

    mockGeolocation.watchPosition.mockImplementation((success, error) => {
      error(timeoutError);
      return 123;
    });

    const { result } = renderHook(() => useJuheGeolocation());

    await act(async () => {
      await result.current.startTracking();
    });

    expect(result.current.error).toBe('Geolocation timeout');
    expect(result.current.isTracking).toBe(false);
  });
});
