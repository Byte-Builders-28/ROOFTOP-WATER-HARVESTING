import requests
from datetime import datetime
from ..db import crud, database

# --- Air Quality (AQI) ---
def get_aqi(db, city="Delhi"):
    url = f"https://api.openaq.org/v2/latest?city={city}"
    response = requests.get(url)
    data = response.json()

    for entry in data.get("results", []):
        for measure in entry.get("measurements", []):
            if measure["parameter"] == "pm25":  # Example AQI value
                crud.save_aqi(
                    db,
                    city=city,
                    aqi=float(measure["value"]),
                    date=datetime.now()
                )
    return {"status": "success", "records": len(data.get("results", []))}



