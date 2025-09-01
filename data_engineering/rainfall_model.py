import pandas as pd
from sklearn.linear_model import LinearRegression
from ..db import crud, session

def train_and_predict_rainfall(csv_path="data/rainfall.csv", subdivision="BIHAR"):
    """
    Train linear regression on rainfall data and predict for each month.
    Returns: list of 12 predicted monthly values for subdivision
    """
    df = pd.read_csv(csv_path)

    # Filter subdivision
    df = df[df["SUBDIVISION"] == subdivision]

    months = ["JAN","FEB","MAR","APR","MAY","JUN",
              "JUL","AUG","SEP","OCT","NOV","DEC"]

    X = df[["YEAR"]]  # Independent variable
    predictions = []

    # Start DB session
    db = session.SessionLocal()

    for month in months:
        y = df[month].fillna(0)  # Handle NaNs if present

        # Train regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict next year (e.g. last year + 1)
        next_year = [[df["YEAR"].max() + 1]]
        pred_value = float(model.predict(next_year)[0])

        predictions.append(pred_value)

        # Save in DB
        crud.save_rainfall_prediction(
            db=db,
            subdivision=subdivision,
            month=month,
            predicted_value=pred_value
        )

    db.close()
    return predictions
