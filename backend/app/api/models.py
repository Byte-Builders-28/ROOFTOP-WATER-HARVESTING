from pydantic import BaseModel
from typing import Optional

class RainRequest(BaseModel):
    area: float
    population: int
    state: str
    city: str
    roof: str

    # Optional fields
    budget: Optional[float] = None


class WaterInput(BaseModel):
    uuid: str
    state: str
    city: str
    tank_cap: int
    current_level: int
    population: int
    avg_need: Optional[int] = 135


# Input for saving WaterQuality
class WaterQualityCreate(BaseModel):
    uuid: str
    ph: int
    tds: int
    diameter: float
    water_depth: float


# Output for reading WaterQuality
class WaterQualityResponse(WaterQualityCreate):
    class Config:
        from_attributes = True
