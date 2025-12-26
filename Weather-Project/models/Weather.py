"""
    This is the Weather model class for the project.
    Handles weather data retrieval from OpenWeatherMap API
"""

from models.Base_model import BaseModel
from Weather.logic import WeatherAPI
from datetime import datetime

class Weather(BaseModel):
    """
    The Weather class represents weather data for a location.
    Inherits from BaseModel.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize a new Weather instance."""
        super().__init__(*args, **kwargs)
        self.username = kwargs.get('username', "")
        self.location = kwargs.get('location', "")
        self.latitude = kwargs.get('latitude', None)
        self.longitude = kwargs.get('longitude', None)
        self.current_weather = kwargs.get('current_weather', None)
        self.hourly_forecast = kwargs.get('hourly_forecast', None)
        self.weekly_forecast = kwargs.get('weekly_forecast', None)
        self.search_timestamp = kwargs.get('search_timestamp', None)
    
    def get_all_weather(self, location):
        """Get all weather data (current, hourly, weekly) for a location."""
        # Get coordinates using the API logic
        coords = WeatherAPI.get_coordinates(location)
        
        if not coords:
            return None
            
        self.latitude = coords['lat']
        self.longitude = coords['lon']
        self.location = coords['location']
        
        # Get weather data using the API logic
        self.current_weather = WeatherAPI.get_current_weather(self.latitude, self.longitude)
        self.hourly_forecast = WeatherAPI.get_hourly_forecast(self.latitude, self.longitude)
        self.weekly_forecast = WeatherAPI.get_weekly_forecast(self.latitude, self.longitude)
        self.search_timestamp = datetime.now().isoformat()
        
        return {
            'location': self.location,
            'current': self.current_weather,
            'hourly': self.hourly_forecast,
            'weekly': self.weekly_forecast
        }
    
    def save_to_history(self, username):
        """Save this weather search to history."""
        self.username = username
        Weather.save()
    
    @classmethod
    def get_user_weather_history(cls, username):
        """Get all weather searches for a specific user."""
        cls.load()
        
        if cls not in cls.objects:
            return []
        
        user_weather = []
        for weather in cls.objects[cls]:
            if weather.username == username:
                user_weather.append(weather)
        
        # Sort by timestamp (newest first)
        return sorted(user_weather, key=lambda w: w.search_timestamp or '', reverse=True)
    
    def to_dict(self):
        """Convert Weather instance to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'current_weather': self.current_weather,
            'hourly_forecast': self.hourly_forecast,
            'weekly_forecast': self.weekly_forecast,
            'search_timestamp': self.search_timestamp,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            '__class__': self.__class__.__name__
        }
    
    def __str__(self):
        """Return string representation of the Weather instance."""
        return f'[{type(self).__name__}] ({self.id}) Location: {self.location}'
