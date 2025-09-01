import requests
from ..db import crud,database
from datetime import datetime
from app.data_engineering.rainfall_model import train_and_predict_rainfall

# --- Rainfall ---

# For testing the rainfall model directly
from app.data_engineering.rainfall_model import train_and_predict_rainfall

predictions = train_and_predict_rainfall("./data_engineering/data/rainfall.csv", subdivision="GOA")
print("Predicted 12-month rainfall:", predictions)


