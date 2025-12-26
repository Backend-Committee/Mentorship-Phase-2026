"""
    Weather API logic to handle Open-Meteo requests.
"""

import requests
from datetime import datetime

class WeatherAPI:
    """Handles interactions with the Open-Meteo API."""
    
    # No API Key needed for Open-Meteo
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
    
    WMO_CODES = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }

    @classmethod
    def _get_description(cls, code):
        return cls.WMO_CODES.get(code, "Unknown")

    @classmethod
    def get_coordinates(cls, location):
        """Get latitude, longitude and formatted location name."""
        try:
            params = {
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            response = requests.get(cls.GEOCODING_URL, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if "results" in data and data["results"]:
                    result = data["results"][0]
                    country = result.get('country', '')
                    name = result['name']
                    return {
                        'lat': result['latitude'],
                        'lon': result['longitude'],
                        'location': f"{name}, {country}" if country else name
                    }
            return None
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return None

    @classmethod
    def get_current_weather(cls, lat, lon):
        """Get current weather data."""
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,cloud_cover,surface_pressure,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min",
                "wind_speed_unit": "ms",
                "timezone": "auto"
            }
            response = requests.get(cls.FORECAST_URL, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current']
                daily = data['daily']
                
                # Get today's min/max (index 0)
                temp_min = daily['temperature_2m_min'][0] if daily and 'temperature_2m_min' in daily else current['temperature_2m']
                temp_max = daily['temperature_2m_max'][0] if daily and 'temperature_2m_max' in daily else current['temperature_2m']

                return {
                    'temp': current['temperature_2m'],
                    'feels_like': current['apparent_temperature'],
                    'temp_min': temp_min,
                    'temp_max': temp_max,
                    'humidity': current['relative_humidity_2m'],
                    'pressure': current['surface_pressure'],
                    'description': cls._get_description(current['weather_code']),
                    'icon': str(current['weather_code']),
                    'wind_speed': current['wind_speed_10m'],
                    'clouds': current['cloud_cover'],
                    'timestamp': datetime.fromisoformat(current['time']) if isinstance(current['time'], str) else datetime.fromtimestamp(current['time'])
                }
            return None
        except Exception as e:
            print(f"Error getting current weather: {e}")
            return None

    @classmethod
    def get_hourly_forecast(cls, lat, lon):
        """Get hourly forecast (next 24h)."""
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "wind_speed_unit": "ms",
                "forecast_days": 2,
                "timezone": "auto"
            }
            response = requests.get(cls.FORECAST_URL, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                hourly = data['hourly']
                hourly_forecast = []
                
                now = datetime.now()
                
                # Collect all future hourly data
                future_data = []
                for i in range(len(hourly['time'])):
                    dt = datetime.fromisoformat(hourly['time'][i])
                    if dt > now:
                        future_data.append({
                            'time': dt.strftime('%H:%M'),
                            'temp': hourly['temperature_2m'][i],
                            'description': cls._get_description(hourly['weather_code'][i]),
                            'icon': str(hourly['weather_code'][i]),
                            'wind_speed': hourly['wind_speed_10m'][i],
                            'humidity': hourly['relative_humidity_2m'][i],
                            'rain': 0
                        })
                
                # Return every 3rd item, up to 8 items (approx 24h coverage with 3h steps)
                return future_data[::3][:8]
            return None
        except Exception as e:
            print(f"Error getting hourly forecast: {e}")
            return None

    @classmethod
    def get_weekly_forecast(cls, lat, lon):
        """Get weekly forecast (5 days)."""
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,wind_speed_10m_max",
                "wind_speed_unit": "ms",
                "forecast_days": 6,
                "timezone": "auto"
            }
            response = requests.get(cls.FORECAST_URL, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                daily = data['daily']
                weekly_forecast = []
                
                for i in range(len(daily['time'])):
                    weekly_forecast.append({
                        'date': daily['time'][i],
                        'temp_min': daily['temperature_2m_min'][i],
                        'temp_max': daily['temperature_2m_max'][i],
                        'temp_avg': (daily['temperature_2m_min'][i] + daily['temperature_2m_max'][i]) / 2,
                        'description': cls._get_description(daily['weather_code'][i]),
                        'icon': str(daily['weather_code'][i]),
                        'humidity': 0,
                        'wind_speed': daily['wind_speed_10m_max'][i]
                    })
                
                return weekly_forecast
            return None
        except Exception as e:
            print(f"Error getting weekly forecast: {e}")
            return None
