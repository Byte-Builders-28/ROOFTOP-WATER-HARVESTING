import requests
from fastapi import APIRouter, Depends
from ..db import crud, database
from datetime import datetime

router = APIRouter()

@router.get("/fetch-groundwater")
def fetch_groundwater(db: database.SessionLocal = Depends(database.get_db)):
    url = "https://indiawris.gov.in/..."   # The groundwater API , but i dont know the exact working one......
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
