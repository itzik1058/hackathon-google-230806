from os import getenv

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from solar.geometry.router import router as geometry_router

app = FastAPI(title="Solar")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(geometry_router, prefix="/geometry")


def run() -> None:
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(getenv("PORT", 8000)),
    )


if __name__ == "__main__":
    run()
