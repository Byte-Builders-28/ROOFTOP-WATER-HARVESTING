# main.py

from fastapi import FastAPI
from .db import models, database
# from app.api.routes import router 
from .api.routes import router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Routers Added...
app.include_router(router, prefix="/api/v1")
# app.include_router(weather.router, prefix="/api")



