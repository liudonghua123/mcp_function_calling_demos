import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str) -> dict:
    """Get current weather for a city using OpenWeather API"""
    # api_key = os.getenv("OPENWEATHER_API_KEY")
    # url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    # response = requests.get(url)
    # response.raise_for_status()
    # return response.json()
    return json.loads('{"coord":{"lon":121.4581,"lat":31.2222},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"base":"stations","main":{"temp":20.92,"feels_like":19.69,"temp_min":20.92,"temp_max":20.92,"pressure":1022,"humidity":24,"sea_level":1022,"grnd_level":1021},"visibility":10000,"wind":{"speed":5,"deg":270},"clouds":{"all":0},"dt":1742525607,"sys":{"type":1,"id":9659,"country":"CN","sunrise":1742507826,"sunset":1742551542},"timezone":28800,"id":1796236,"name":"Shanghai","cod":200}')

def get_current_datetime() -> str:
    """Get current datetime in ISO format"""
    return datetime.now().isoformat()
