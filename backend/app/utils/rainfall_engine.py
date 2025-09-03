import requests
from ..db import crud,database
from datetime import datetime
from data_engineering.rainfall_model import train_and_predict_rainfall



# --- Rainfall ---

from utils.weather import get_info_from_location
from utils.get_region import classify_location
from data_engineering.region_list import get_distinct_subdivisions
from utils.get_rain import get_mean_rainfall
from dotenv import load_dotenv


predictions = train_and_predict_rainfall("./data_engineering/data/rainfall.csv", subdivision="GOA")
print("Predicted 12-month rainfall:", predictions)

reg = ['ANDAMAN & NICOBAR ISLANDS', 'ARUNACHAL PRADESH', 'ASSAM & MEGHALAYA', 'BIHAR', 'CHHATTISGARH', 'COASTAL ANDHRA PRADESH', 'COASTAL KARNATAKA', 'EAST MADHYA PRADESH', 'EAST RAJASTHAN', 'EAST UTTAR PRADESH', 'GANGETIC WEST BENGAL', 'GUJARAT REGION', 'HARYANA DELHI & CHANDIGARH', 'HIMACHAL PRADESH', 'JAMMU & KASHMIR', 'JHARKHAND', 'KERALA', 'KONKAN & GOA', 'LAKSHADWEEP', 'MADHYA MAHARASHTRA', 'MATATHWADA', 'NAGA MANI MIZO TRIPURA', 'NORTH INTERIOR KARNATAKA', 'ORISSA', 'PUNJAB', 'RAYALSEEMA', 'SAURASHTRA & KUTCH', 'SOUTH INTERIOR KARNATAKA', 'SUB HIMALAYAN WEST BENGAL & SIKKIM', 'TAMIL NADU', 'TELANGANA', 'UTTARAKHAND', 'VIDARBHA', 'WEST MADHYA PRADESH', 'WEST RAJASTHAN', 'WEST UTTAR PRADESH']

def get_RTWH(
    area_m2: float,
    population: int,
    groundwater_capacity: float,
    state: str,
    city: str,
    budget: float = None,
    tank_capacity: float = None
):
    """
    Get Rainwater Tank + Water Harvesting (RTWH) recommendation.
    
    Args:
        area_m2 (float): Roof/land area in square meters.
        population (int): Number of people using the water.
        groundwater_capacity (float): Groundwater capacity in liters.
        state (str): State where the system will be implemented.
        city (str): City where the system will be implemented.
        budget (float, optional): Budget in currency units.
        tank_capacity (float, optional): Tank capacity in liters.

    Returns:
        dict: Recommendation result with feasibility, system type, cost, etc.
    """
    
    # TODO: fetch rainfall based on state + city (API integration)
    # rainfall_mm = get_rainfall_from_location(state, city)
 
    info = get_info_from_location(state=state, city=city)
    temp = info["temperature"]            # °C
    humidity = info["humidity"]        # %

    region = classify_location(f"{city}, {state}", reg)

    # For now, just placeholder values
    rainfall_mm = get_mean_rainfall(region)  

    from algo.get_task import recommend_system
    
    return recommend_system(
        area_m2=area_m2,
        rainfall_mm=rainfall_mm,
        temp=temp,
        humidity=humidity,
        population=population,
        budget=budget,
        tank_capacity=tank_capacity,
        groundwater_capacity=groundwater_capacity
    )
