import os
from dotenv import load_dotenv
import requests

from backend.app.utils.location import get_location_details

def get_info_from_location(state: str, city: str):
    """
    Uses city + state to fetch coordinates (via Nominatim) 
    then queries OpenWeather for temp & humidity.
    """
    # Load API key from .env
    load_dotenv()
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    
    # Get latitude/longitude
    location = get_location_details(f"{city}, {state}")
    if not location:
        return None

    lat, lon = location["latitude"], location["longitude"]

    # Query OpenWeather
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    resp = requests.get(url).json()

    temp = resp["main"]["temp"]
    humidity = resp["main"]["humidity"]

    return {
        "temperature": temp,
        "humidity": humidity,
        "address": location["address"]
    }