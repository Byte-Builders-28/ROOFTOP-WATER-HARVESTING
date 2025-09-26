from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd

from . import models

# process dataframe 
def preprocess_and_average(data, time_col="date", value_col="value", freq="D"):
    """
 It Convert list of dicts to DataFrame, then resample to avg values. ( for now it's like avg value but i have to thought what to add in future)
    time_col: timestamp column ....value_col: numeric column....  freq: 'D' for daily, 'H' for hourly
    """
    df = pd.DataFrame(data)
    df[time_col] = pd.to_datetime(df[time_col])
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    # Drop invalid
    df = df.dropna(subset=[value_col])

    # Resample & average
    df = df.set_index(time_col).resample(freq).mean().reset_index()
    return df


# Groundwater
def save_groundwater(db: Session, records: list):
    df = preprocess_and_average(records, time_col="date", value_col="level", freq="D")

    for _, row in df.iterrows():
        db_record = models.GroundWater(
            location=records[0].get("location", "Unknown"),  # use first location
            level=row["level"],
            date=row["date"].to_pydatetime()
        )
        db.add(db_record)
    db.commit()


# Rainfall
def save_rainfall_prediction(db, subdivision: str, month: str, predicted_value: float):
    prediction = models.RainfallPrediction(
        subdivision=subdivision,
        month=month,
        predicted_rainfall=predicted_value
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

# Temperature 
def save_temperature(db: Session, records: list):
    df = preprocess_and_average(records, time_col="date", value_col="temperature", freq="D")

    for _, row in df.iterrows():
        db_record = models.Temperature(
            location=records[0].get("location", "Unknown"),
            temperature=row["temperature"],
            date=row["date"].to_pydatetime()
        )
        db.add(db_record)
    db.commit()


# Soil Moisture 
def save_soil_moisture(db: Session, records: list):
    df = preprocess_and_average(records, time_col="date", value_col="moisture", freq="D")

    for _, row in df.iterrows():
        db_record = models.SoilMoisture(
            location=records[0].get("location", "Unknown"),
            moisture=row["moisture"],
            date=row["date"].to_pydatetime()
        )
        db.add(db_record)
    db.commit()


#  AQI 
def save_aqi(db: Session, records: list):
    df = preprocess_and_average(records, time_col="date", value_col="aqi", freq="D")

    for _, row in df.iterrows():
        db_record = models.AQI(
            location=records[0].get("location", "Unknown"),
            aqi=row["aqi"],
            date=row["date"].to_pydatetime()
        )
        db.add(db_record)
    db.commit()


#  Humidity 
def save_humidity(db: Session, records: list):
    df = preprocess_and_average(records, time_col="date", value_col="humidity", freq="D")

    for _, row in df.iterrows():
        db_record = models.Humidity(
            location=records[0].get("location", "Unknown"),
            humidity=row["humidity"],
            date=row["date"].to_pydatetime()
        )
        db.add(db_record)
    db.commit()
    
def save_water_quality(db: Session, data):
    """
    Insert or update a water quality record for a given UUID.
    If the UUID exists, update its values. Otherwise, insert new.
    """
    db_item = db.query(models.WaterQuality).filter(models.WaterQuality.uuid == data.uuid).first()

    if db_item:
        # Update existing row
        db_item.ph = data.ph
        db_item.tds = data.tds
        db_item.diameter = data.diameter
        db_item.water_depth = data.water_depth
    else:
        # Insert new row
        db_item = models.WaterQuality(
            uuid=data.uuid,
            ph=data.ph,
            tds=data.tds,
            diameter=data.diameter,
            water_depth=data.water_depth
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_item)
    return db_item

def get_water_quality(db: Session, uuid: str):
    return db.query(models.WaterQuality).filter(models.WaterQuality.uuid == uuid).first()
