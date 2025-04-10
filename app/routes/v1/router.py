from fastapi import APIRouter

from app.routes.v1.chess_routes import chess_router

api_router = APIRouter()
api_router.include_router(chess_router)