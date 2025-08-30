import requests
from ..db import crud, database
from datetime import datetime

def get_groundwater(db):
    # The groundwater API , but i dont know the exact working one......
    url = "https://indiawris.gov.in/..."
    response = requests.get(url)
    data = response.json()

    for entry in data["items"]:   # Always adjust if needed....
        crud.save_groundwater(
            db,
            location=entry["location"],
            level=float(entry["level"]),
            date=datetime.strptime(entry["date"], "%Y-%m-%d")
        )
    return {"status": "success", "records": len(data["items"])}
