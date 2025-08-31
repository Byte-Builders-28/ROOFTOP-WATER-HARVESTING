import requests
from datetime import datetime
from ..db import crud, database

# --- Soil Moisture ---
def get_soil_moisture(db):
    # url = "https://api.agromonitoring.com/agro/1.0/soil?lat=28.6&lon=77.2&appid=YOUR_API_KEY"
    url = "https://indiawris.gov.in/swagger-ui/index.html#/Data%20API%20Based%20On%20Admin%20Hierarchy/getSoilMoistureByState"
    response = requests.get(url)
    data = response.json()

    if "moisture" in data:
        crud.save_soil_moisture(
            db,
            location="Delhi",  # Or fetch dynamically
            moisture=float(data["moisture"]),
            date=datetime.now()
        )
        return {"status": "success", "records": 1}
    return {"status": "failed", "records": 0}