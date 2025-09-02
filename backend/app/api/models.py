from pydantic import BaseModel
from typing import Optional

class RainRequest(BaseModel):
    area_m2: float
    population: int
    groundwater_capacity: float
    state: str
    city: str
    
    # Optional fields
    budget: Optional[float] = None
    tank_capacity: Optional[float] = None
