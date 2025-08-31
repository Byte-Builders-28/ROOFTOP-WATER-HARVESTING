from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

# Ground Water Level Table
class GroundWaterLevel(Base):
    __tablename__ = "ground_water_level"
    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String)
    station_name = Column(String)
    state = Column(String)
    district = Column(String)
    data_value = Column(Float)
    data_time = Column(DateTime)

# Rainfall Table
class Rainfall(Base):
    __tablename__ = "rainfall"
    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String)
    station_name = Column(String)
    state = Column(String)
    district = Column(String)
    data_value = Column(Float)
    data_time = Column(DateTime)

# Temperature Table
class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String)
    station_name = Column(String)
    state = Column(String)
    district = Column(String)
    data_value = Column(Float)
    data_time = Column(DateTime)

# Humidity Table
class Humidity(Base):
    __tablename__ = "humidity"
    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String)
    station_name = Column(String)
    state = Column(String)
    district = Column(String)
    data_value = Column(Float)
    data_time = Column(DateTime)

# Soil Moisture Table
class SoilMoisture(Base):
    __tablename__ = "soil_moisture"
    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String)
    station_name = Column(String)
    state = Column(String)
    district = Column(String)
    data_value = Column(Float)
    data_time = Column(DateTime)

# Air Quality Index Table
class AQI(Base):
    __tablename__ = "aqi"
    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String)
    station_name = Column(String)
    state = Column(String)
    district = Column(String)
    data_value = Column(Float)
    data_time = Column(DateTime)
