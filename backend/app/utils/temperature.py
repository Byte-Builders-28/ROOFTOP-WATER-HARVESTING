import requests
from datetime import datetime
from ..db import crud, database

# --- Temperature ---
def get_temperature(db, city="Delhi"):
    url = f"https://indiawris.gov.in/swagger-ui/index.html#/Data%20API%20Based%20On%20Admin%20Hierarchy/getMTTemp"
    response = requests.get(url)
    data = response.json()

    if "current" in data:
        crud.save_temperature(
            db,
            city=city,
            temp=float(data["current"]["temperature_2m"]),
            date=datetime.now()
        )
        return {"status": "success", "records": 1}
    return {"status": "failed", "records": 0}

