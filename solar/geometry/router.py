from fastapi import APIRouter

from solar.geometry.models import BuildingSolar
from solar.geometry.service import solar_by_address, solar_by_point

router = APIRouter()


@router.get("/from-address")
async def geometry_by_address(
    address: str,
    radius: int = 20,
) -> BuildingSolar:
    return solar_by_address(address, radius)


@router.get("/from-point")
async def geometry_from_point(
    latitude: float,
    longitude: float,
    radius: int = 20,
) -> BuildingSolar:
    return solar_by_point((latitude, longitude), radius)
