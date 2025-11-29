import os
from dotenv import load_dotenv
import requests
from collections import defaultdict


from backend.app.utils.location import get_location_details


def get_info_from_location(state: str, city: str):
    """
    Uses city + state to fetch coordinates (via Nominatim) 
    then queries OpenWeather for temp & humidity.
    """
    print(f"[DEBUG] get_info_from_location called with state={state}, city={city}")

    # Load API key
    load_dotenv()
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not API_KEY:
        print("[ERROR] OPENWEATHER_API_KEY not found in .env")
        return None

    # Get latitude/longitude
    location = get_location_details(f"{city}, {state}")
    print(f"[DEBUG] Location details: {location}")

    if not location:
        print(f"[ERROR] Could not resolve coordinates for {city}, {state}")
        return None

    lat, lon = location.get("latitude"), location.get("longitude")
    if lat is None or lon is None:
        print(f"[ERROR] Missing latitude/longitude in location: {location}")
        return None

    # Query OpenWeather
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    print(f"[DEBUG] OpenWeather request URL: {url}")

    try:
        resp = requests.get(url, timeout=10)
        print(f"[DEBUG] OpenWeather raw status: {resp.status_code}")
        data = resp.json()
        print(f"[DEBUG] OpenWeather response JSON: {data}")
    except Exception as e:
        print(f"[ERROR] Request to OpenWeather failed: {e}")
        return None

    # Extract required fields
    try:
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
    except KeyError as e:
        print(f"[ERROR] Missing expected key in response: {e}, data={data}")
        return None

    result = {
        "temperature": temp,
        "humidity": humidity,
        "address": location.get("address"),
    }
    print(f"[DEBUG] Final weather info: {result}")

    return result

def get_next5days_rain(state: str, city: str) -> list[float]:
    load_dotenv()
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not API_KEY:
        print("[ERROR] OPENWEATHER_API_KEY not found")
        return []

    location = get_location_details(f"{city}, {state}")
    if not location:
        return []

    lat, lon = location["latitude"], location["longitude"]

    url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("[ERROR] OpenWeather request failed:", e)
        return []

    rain_by_day = defaultdict(float)
    today = date.today()

    for entry in data.get("list", []):
        ts = entry.get("dt")
        if not ts:
            continue

        day = datetime.utcfromtimestamp(ts).date()

        # Skip today; we want full future days only
        if day <= today:
            continue

        rain_3h = entry.get("rain", {}).get("3h", 0.0)
        rain_by_day[day] += rain_3h

    # Take next 5 days in order
    next_5_days = sorted(rain_by_day.items())[:5]
    result = [round(rain, 2) for _, rain in next_5_days]

    print("[DEBUG] Next 5 days rainfall list:", result)
    return result