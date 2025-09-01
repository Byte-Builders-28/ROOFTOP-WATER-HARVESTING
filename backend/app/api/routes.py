from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import crud, database
from datetime import datetime

from ..utils.groundwater_engine import get_groundwater
from ..utils.rainfall_engine import get_rainfall

router = APIRouter()

@router.get("/")
def read_root():
   return {"message" : "FastApi is running"}
   
@router.get("/fetch-groundwater")
def fetch_groundwater(db: Session = Depends(database.get_db)):
   return get_groundwater(db)


@router.get("/fetch-weather")
def fetch_weather(db: Session = Depends(database.get_db)):
	return get_rainfall(db)