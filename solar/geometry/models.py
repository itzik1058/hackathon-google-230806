from pydantic import BaseModel


class BuildingGeometry(BaseModel):
    coords: list[tuple[float, float]]
    area: float


class BuildingSolar(BaseModel):
    geometry: BuildingGeometry
    year_energy_kwh: float
    construction_cost: float
    yearly_saving_nis: list[float]
