from pydantic import BaseModel

class RainRequest(BaseModel):
    area_m2: float
    population: int
    budget: float | None = None
    tank_capacity: int = 20000
    groundwater_capacity: int = 50000
