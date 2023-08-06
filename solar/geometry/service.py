import logging
from pathlib import Path
from typing import Any

from fastapi import HTTPException
from numpy import float64, loadtxt
from osmnx import features_from_address, features_from_point
from shapely import Point, Polygon

from solar.geometry.constants import (
    AREA_UTILIZATION,
    CONSTRUCTION_COST,
    SOLAR_EFFICIENCY,
    SOLAR_PRICE_NIS,
    TAX_RATE,
)
from solar.geometry.models import BuildingGeometry, BuildingSolar


def solar_by_address(
    address: str,
    radius: int,
) -> BuildingSolar:
    try:
        buildings = features_from_address(
            address,
            tags={"building": True},
            dist=radius,
        )
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=404, detail="Address not found")
    return solar_features(buildings)


def solar_by_point(
    point: tuple[float, float],
    radius: int,
) -> BuildingSolar:
    try:
        buildings = features_from_point(
            point,
            tags={"building": True},
            dist=radius,
        )
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=404, detail="Address not found")
    return solar_features(buildings)


def building_features(buildings: Any) -> BuildingGeometry:
    building = buildings.iloc[0]
    building_3857 = buildings.to_crs("epsg:3857").iloc[0]
    coords: list[tuple[float, float]] = []
    if isinstance(building.geometry, Polygon):
        coords = [(point[1], point[0]) for point in building.geometry.exterior.coords]
    elif isinstance(building.geometry, Point):
        coords = [(building.geometry.y, building.geometry.x)]
    area: float = building_3857.geometry.area
    return BuildingGeometry(
        coords=coords,
        area=area,
    )


def total_solar_irradiance(latitude: float, longitude: float) -> float:
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


def solar_features(buildings: Any) -> BuildingSolar:
    geometry = building_features(buildings)
    tsi = total_solar_irradiance(*geometry.coords[0])
    yearly_energy_kwh = tsi * geometry.area * AREA_UTILIZATION * SOLAR_EFFICIENCY
    year_saving_nis = yearly_energy_kwh * SOLAR_PRICE_NIS * (1 + TAX_RATE)
    construction_cost = CONSTRUCTION_COST * geometry.area
    yearly_saving_nis = [
        year_saving_nis * year - construction_cost for year in range(15)
    ]
    return BuildingSolar(
        geometry=geometry,
        yearly_saving_nis=yearly_saving_nis,
    )
