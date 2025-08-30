from fastapi import APIRouter, Depends
from ..db import crud, database
from datetime import datetime

from    ..services.groundwater_engine import get_groundwater
from    ..services.rainfall_engine import get_weather

router = APIRouter()


@router.get("/fetch-groundwater")
def fetch_groundwater(db: database.SessionLocal = Depends(database.get_db)):
   return get_groundwater(db)


@router.get("/fetch-weather")
def fetch_weather(db: database.SessionLocal = Depends(database.get_db)):
	return get_weather(db)