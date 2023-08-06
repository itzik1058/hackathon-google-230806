import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from osmnx import features_from_address

from solar.models import GeometryResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/geometry")
def geometry(address: str) -> GeometryResponse:
    try:
        buildings = features_from_address(
            address,
            tags={"building": True},
            dist=15,
        )
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=404, detail="Address not found")
    building = buildings.iloc[0]
    building_3857 = buildings.to_crs("epsg:3857").iloc[0]
    coords = list(building.geometry.exterior.coords)
    area = building_3857.geometry.area
    return GeometryResponse(coords=coords, area=area)


def run() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
