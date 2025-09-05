import pickle
import numpy as np
import os

# Load model
MODEL_PATH = "ML_models/water_risk_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("⚠️ Train the model first using train.py!")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def predict_water_risk(tank_cap, current_level, dwellers, avg_need, rain_next7, dry_days):
    """Predict water risk using trained DecisionTree model"""
    X = np.array([[tank_cap, current_level, dwellers, avg_need, rain_next7, dry_days]])
    risk = model.predict(X)[0]

    # Suggestions
    if risk == 1:
        suggestion = "⚠️ Risk: Low storage + less rainfall ahead. Save water urgently!"
        tips = [
            "Use buckets instead of showers",
            "Avoid car washing",
            "Recycle greywater for gardening",
            "Prioritize drinking and cooking needs"
        ]
    else:
        suggestion = "✅ Safe: Tank level and rainfall forecast are sufficient."
        tips = [
            "Maintain moderate use",
            "Harvest extra rain if possible",
            "Increse Groundwater recharge",
            "Monitor weekly usage"
        ]

    return {"risk": int(risk), "suggestion": suggestion, "tips": tips}
