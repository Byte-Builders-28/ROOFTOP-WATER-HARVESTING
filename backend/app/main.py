# main.py
from fastapi import FastAPI
from app.api.routes import router  

app = FastAPI()

# include the routes
app.include_router(router, prefix="/api", tags=["My Routes"])
