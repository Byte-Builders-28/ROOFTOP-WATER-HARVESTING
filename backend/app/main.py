# main.py
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

from .db import models, database
# from app.api.routes import router 
from .api.routes import router


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost:8000",   
    "https://yourdomain.com",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # list of allowed origins
    allow_credentials= False,
    allow_methods=["*"],            # allow all HTTP methods
    allow_headers=["*"],            # allow all headers
)

# Absolute path to the 'webar' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
webar_dir = os.path.join(current_dir, "../webar")

# Mount static files at /webar
app.mount("/webar", StaticFiles(directory=webar_dir), name="webar")


# Routers Added
app.include_router(router)
