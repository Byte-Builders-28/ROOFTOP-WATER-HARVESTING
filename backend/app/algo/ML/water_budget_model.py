# water_budget_model.py
import pickle
import numpy as np
import os

MODEL_PATH = "backend/app/algo/ML/ML_models/water_risk_model.pkl"

# Load model at import
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Train the model first using train.py!")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def predict_water_risk(tank_cap, current_level, dwellers, avg_need, rain_next7, dry_days):
    """
    Predict water risk using trained DecisionTree model
    Returns risk, suggestion, and tips
    """
    X = np.array([[tank_cap, current_level, dwellers, avg_need, rain_next7, dry_days]])
    risk = model.predict(X)[0]

    # Suggestions based on risk
    if risk == 1:
        suggestion = "Risk: Low storage + less rainfall ahead. Save water urgently!"
        tips = [
            "Use buckets instead of showers",
            "Avoid washing vehicles",
            "Recycle greywater for gardening",
            "Prioritize drinking and cooking needs",
            "Cover tanks to reduce evaporation"
        ]
    else:
        suggestion = "Safe: Tank level and rainfall forecast are sufficient."
        tips = [
            "Maintain moderate use",
            "Harvest extra rain if possible",
            "Increase groundwater recharge (RTRWH/AR)",
            "Monitor weekly usage",
            "Clean rooftop filters regularly"
        ]

    return {"risk": int(risk), "suggestion": suggestion, "tips": tips}
