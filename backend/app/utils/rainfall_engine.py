import requests
from ..db import crud,database
from datetime import datetime
from data_engineering.rainfall_model import train_and_predict_rainfall

# --- Rainfall ---

predictions = train_and_predict_rainfall("./data_engineering/data/rainfall.csv", subdivision="GOA")
print("Predicted 12-month rainfall:", predictions)

def get_RTWH(db):
    pass
