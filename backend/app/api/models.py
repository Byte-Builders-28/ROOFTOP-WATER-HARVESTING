from pydantic import BaseModel
from typing import Optional

class RainRequest(BaseModel):
    area: float
    population: int
    # groundwater_capacity: float
    state: str
    city: str
    roof: str

    # Optional fields
    budget: Optional[float] = None
class WaterInput(BaseModel):
    tank_cap: int
    current_level: int
    dwellers: int
    avg_need: int
    rain_next7: float
    dry_days: int
