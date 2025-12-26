import os
from dotenv import load_dotenv
import requests
import sys

class Weather:
    def __init__(self, city=""):
        self._setAPI_KEY()
        self.city = city

    def _setAPI_KEY(self):
        load_dotenv()   
        self.__API_KEY = os.getenv('API_KEY')
    def setCity(self, city):
        self.city = city.lower().strip()
    def getWeather(self):
        location = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={self.city}&appid={self.__API_KEY}')
        if location:
            data = location.json()[0]
            lat, lon = data["lat"], data["lon"]

            weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.__API_KEY}')
            if weather:
                return weather.json()
            else:
                sys.exit("Error in getting Weather")

        else:
            sys.exit("Error in getting city location")
