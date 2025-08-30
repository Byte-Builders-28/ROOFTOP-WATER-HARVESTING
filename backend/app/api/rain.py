import requests
from fastapi import APIRouter, Depends
from ..db import crud, database
from datetime import datetime

router = APIRouter()

@router.get("/fetch-weather")
def fetch_weather(db: database.SessionLocal = Depends(database.get_db)):
    url = "https://mausam.imd.gov.in/api/nowcast_district_api.php?id=1"   # API check , and find the working one......
    response = requests.get(url)
    data = response.json()

    for entry in data["districts"]:   # adjust key
        crud.save_weather(
            db,
            district=entry["name"],
            forecast=entry["forecast"],
            timestamp=datetime.now()
        )
    return {"status": "success", "records": len(data["districts"])}
