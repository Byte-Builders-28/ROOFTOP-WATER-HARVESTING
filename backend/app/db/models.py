from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class GroundWater(Base):
    __tablename__ = "groundwater"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    level = Column(Float)
    date = Column(DateTime)

class Rain(Base):
    __tablename__ = "rain"
    id = Column(Integer, primary_key=True, index=True)
    district = Column(String)
    forecast = Column(String)
    timestamp = Column(DateTime)
