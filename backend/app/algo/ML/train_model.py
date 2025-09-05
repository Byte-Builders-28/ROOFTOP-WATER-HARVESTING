import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
import os

def train_model():
    # Load dataset
    df = pd.read_csv("...data_engineering/data/synthetic_training.csv")

    # Features and target
    X = df[["tank_cap", "current_level", "dwellers", "avg_need", "rain_next7", "dry_days"]]
    y = df["risk"]

    # Train model
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X, y)

    # Ensure models dir exists
    os.makedirs("models", exist_ok=True)

    # Save model
    with open("ML_models/water_risk_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("✅ Model trained and saved at models/water_risk_model.pkl")

if __name__ == "__main__":
    train_model()
