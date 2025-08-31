import requests
from datetime import datetime
from ..db import crud, database

# --- Humidity ---
def get_humidity(db, city="Delhi"):
    url = f"https://api.open-meteo.com/v1/forecast?latitude=28.6&longitude=77.2&current=relative_humidity_2m"
    response = requests.get(url)
    data = response.json()

    if "current" in data:
        crud.save_humidity(
            db,
            city=city,
            humidity=float(data["current"]["relative_humidity_2m"]),
            date=datetime.now()
        )
        return {"status": "success", "records": 1}
    return {"status": "failed", "records": 0}
