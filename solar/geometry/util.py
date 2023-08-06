from pathlib import Path
from typing import Any

from numpy import float64, loadtxt
from shapely import Point, Polygon

from solar.geometry.models import GeometryResponse


def building_features(buildings: Any) -> GeometryResponse:
    building = buildings.iloc[0]
    building_3857 = buildings.to_crs("epsg:3857").iloc[0]
    coords: list[tuple[float, float]] = []
    if isinstance(building.geometry, Polygon):
        coords = [(point[1], point[0]) for point in building.geometry.exterior.coords]
    elif isinstance(building.geometry, Point):
        coords = [(building.geometry.y, building.geometry.x)]
    area: float = building_3857.geometry.area
    ir = irradiance(*coords[0])
    return GeometryResponse(coords=coords, area=area, irradiance=ir)


def irradiance(latitude: float, longitude: float) -> float:
    file_name = Path("resources/GTI.asc")
    with file_name.open() as file_h:
        lines = file_h.read().splitlines()
    # ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value
    header = dict(map(str.split, lines[:6]))
    data_array = loadtxt(lines[6:], dtype=float64)

    nrows = int(header["nrows"])
    xllcorner = float(header["xllcorner"])
    yllcorner = float(header["yllcorner"])
    cellsize = float(header["cellsize"])
    x = int((latitude - xllcorner) // cellsize)
    y = int((yllcorner + nrows * cellsize - longitude) / cellsize)
    return float(data_array[x][y])
