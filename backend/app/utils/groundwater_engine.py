import requests
from ..db import crud, database
from datetime import datetime


# --- Groundwater ---
def get_groundwater(db):
    url = "https://indiawris.gov.in/swagger-ui/index.html#/Data%20API%20Based%20On%20Admin%20Hierarchy/getGroundWaterLevel"   # Replace with actual working API
    response = requests.get(url)
    data = response.json()
    
    print(response.status_code)

    for entry in data.get("items", []):   # Adjust based on API response
        crud.save_groundwater(
            db,
            location=entry.get("location"),
            level=float(entry.get("level", 0)),
            date=datetime.strptime(entry.get("date"), "%Y-%m-%d")
        )
    return {"status": "success", "records": len(data.get("items", []))}
