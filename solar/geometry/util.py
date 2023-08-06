from typing import Any

from shapely import Point, Polygon

from solar.models import GeometryResponse


def building_features(buildings: Any) -> GeometryResponse:
    building = buildings.iloc[0]
    building_3857 = buildings.to_crs("epsg:3857").iloc[0]
    coords: list[tuple[float, float]] = []
    if isinstance(building.geometry, Polygon):
        coords = [(point[1], point[0]) for point in building.geometry.exterior.coords]
    elif isinstance(building.geometry, Point):
        coords = [(building.geometry.y, building.geometry.x)]
    area: float = building_3857.geometry.area
    return GeometryResponse(coords=coords, area=area)
