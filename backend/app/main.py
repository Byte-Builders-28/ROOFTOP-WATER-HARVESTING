# main.py

from fastapi import FastAPI
from .db import models, database
from app.api.routes import router 
from .api import groundwater, weather

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Routers Added...
app.include_router(groundwater.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
