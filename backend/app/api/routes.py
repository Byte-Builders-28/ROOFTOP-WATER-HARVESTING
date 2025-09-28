from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from ..db import crud, database
from .auth import create_access_token, verify_password, get_password_hash, get_current_user
from datetime import datetime

from ..utils.rainfall_engine import get_RTWH
from ..utils.weather import get_next5days_rain

from .models import RainRequest, WaterInput, WaterQualityCreate, WaterQualityResponse
from ..algo.ML.water_budget_model import predict_water_risk

router = APIRouter(prefix="/api")

@router.get("/")
def read_root():
   return {"message" : "FastApi is running"}

@router.get("/checkup")
def read_root():
   return {"message" : "Awake"}

from typing import Optional
from ..utils.location import get_location_details, get_address_from_coords  # your functions


@router.get("/geocode")
def geocode(
    address: Optional[str] = Query(None, description="Address string for forward geocoding"),
    lat: Optional[float] = Query(None, description="Latitude for reverse geocoding"),
    lng: Optional[float] = Query(None, description="Longitude for reverse geocoding")
):
    """
    Single geocode route:
    - Forward mode: provide 'address' → returns coordinates
    - Reverse mode: provide 'lat' and 'lng' → returns address details
    """
    if address:
        result = get_location_details(address)
        if not result:
            raise HTTPException(status_code=404, detail=f"Could not find coordinates for: {address}")
        return {"mode": "forward", **result}
    
    if lat is not None and lng is not None:
        result = get_address_from_coords(lat, lng)
        if not result:
            raise HTTPException(status_code=404, detail=f"Could not find address for coordinates: {lat}, {lng}")
        return {"mode": "reverse", **result}
    
    raise HTTPException(status_code=400, detail="Provide either 'address' or 'lat' and 'lng'")

@router.post("/get_res")
def get_recommendation(req: RainRequest):
    area_m2 = req.area * 0.092903
    result = get_RTWH(
        area_m2=area_m2,
        population=req.population,
        budget=req.budget,
        state=req.state,
        city=req.city,
        rooftype=req.roof
    )
    return result

@router.post("/ml/predict")
def get_prediction(data: WaterInput, db: Session = Depends(database.get_db)):
    # Fetch rain forecast
    rain_next7 = get_next5days_rain(data.state, data.city)
    dry_days = 0 if max(rain_next7) > 0 else 7

    # Fetch water quality from DB using UUID
    quality = crud.get_water_quality(db, data.uuid)
    if not quality:
        raise HTTPException(status_code=404, detail="Water quality data not found for this UUID")

    # Call updated predict_water_risk with ph and tds
    result = predict_water_risk(
        tank_cap=data.tank_cap,
        current_level=data.current_level,
        dwellers=data.population,
        avg_need=data.avg_need,
        rain_next7_list=rain_next7,
        dry_days=dry_days,
        ph=quality.ph,
        tds=quality.tds
    )
    return result


# -------------------------------
# 💧 Water Quality Routes
# -------------------------------
@router.post("/water/", response_model=WaterQualityResponse)
def save_water_quality_route(data: WaterQualityCreate, db: Session = Depends(database.get_db)):
    return crud.save_water_quality(db, data)

@router.get("/water/{uuid}", response_model=WaterQualityResponse)
def read_water_quality_route(uuid: str, db: Session = Depends(database.get_db)):
    db_item = crud.get_water_quality(db, uuid)
    if not db_item:
        raise HTTPException(status_code=404, detail="Water quality data not found")
    return db_item
