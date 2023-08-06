from pydantic import BaseModel


class GeometryResponse(BaseModel):
    coords: list[tuple[float, float]]
    area: float
    irradiance: float
