import os
from dotenv import load_dotenv
import requests
import sys

class Weather:
    def __init__(self, city=""):
        self._getAPIKeyFromENV()
        self.city = city

    def _getAPIKeyFromENV(self):
        load_dotenv()
        self.__API_KEY = os.getenv('API_KEY')
    def setCity(self, city):
        self.city = city.lower().strip()

    def _getCoordinatesFromCityName(self):
        coordinates = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={self.city}&appid={self.__API_KEY}')
        if coordinates:
            data = coordinates.json()[0]
            return data["lat", "lon"]

        sys.exit("Unable to get coordinates")

    def getForecast(self):
        lat, lon = self._getCoordinatesFromCityName()
        weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.__API_KEY}')
        if weather:
            return weather.json()
        else:
            sys.exit("Error in getting Weather")
