from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db import crud, database
from .auth import create_access_token, verify_password, get_password_hash, get_current_user
from datetime import datetime

from ..utils.rainfall_engine import get_RTWH

from .models import RainRequest

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

# # Fake user db (later you’ll use your actual database)
# fake_user = {
#     "username": "rishabh",
#     "hashed_password": get_password_hash("mypassword")
# }

router = APIRouter()

@router.get("/")
def read_root():
   return {"message" : "FastApi is running"}
   
# @router.get("/fetch-groundwater")
# def fetch_groundwater(db: Session = Depends(database.get_db)):
#    return get_groundwater(db)

@router.post("/recommend")
def get_recommendation(req: RainRequest):
    area_m2 = req.area * 0.092903
    result = get_RTWH(
        area_m2=area_m2,
        population=req.population,
        budget=req.budget,
        tank_capacity=req.tank_capacity,
        groundwater_capacity=req.groundwater_capacity,
        state = req.state,
        city = req.city
    )   
    return result

# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     if form_data.username != fake_user["username"] or not verify_password(form_data.password, fake_user["hashed_password"]):
#         raise HTTPException(status_code=400, detail="Invalid username or password")
    
#     access_token = create_access_token(data={"sub": form_data.username})
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/profile")
# def read_profile(current_user: str = Depends(get_current_user)):
#     return {"msg": f"Hello {current_user}, welcome to your profile!"}