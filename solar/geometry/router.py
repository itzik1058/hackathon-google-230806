import logging

from fastapi import APIRouter, HTTPException
from osmnx import features_from_address, features_from_point

from solar.geometry.util import building_features
from solar.models import GeometryResponse

router = APIRouter()


@router.get("/from-address")
async def geometry_by_address(
    address: str,
    radius: int = 20,
) -> GeometryResponse:
    try:
        buildings = features_from_address(
            address,
            tags={"building": True},
            dist=radius,
        )
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=404, detail="Address not found")
    return building_features(buildings)


@router.get("/from-point")
async def geometry_from_point(
    latitude: float,
    longitude: float,
    radius: int = 20,
) -> GeometryResponse:
    try:
        buildings = features_from_point(
            (latitude, longitude),
            tags={"building": True},
            dist=radius,
        )
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=404, detail="Address not found")
    return building_features(buildings)
