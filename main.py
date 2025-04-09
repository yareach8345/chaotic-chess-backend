import sys

import uvicorn
from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI, Depends

from app.core.container import Container
from app.dto.game_init_dto import GameInitDTO
from app.routes.v1.router import api_router
from app.services.chess_service import ChessService

app = FastAPI(
    title="Chaotic Chess",
    description="Chaotic Chess routes",
    version="0.0.0",
)

app.include_router(api_router, prefix="/routes/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    container = Container()
    container.wire([sys.modules[__name__]])
    uvicorn.run(app, port=8000)