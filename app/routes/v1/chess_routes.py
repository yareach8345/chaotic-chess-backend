from typing import List, Annotated, Any, Coroutine

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, Cookie, Request, HTTPException

from app.core.container import Container
from app.dto.game_info_dto import GameInfoDTO
from app.dto.game_init_dto import GameInitDTO
from app.dto.move_dto import MoveDto
from app.dto.turn_result_dto import TurnResultDTO
from app.services.chess_service import ChessService

chess_router = APIRouter(prefix="/game")


@chess_router.post("/")
@inject
async def init_game(request: Request, response: Response, chess_service: ChessService = Depends(Provide[Container.chess_service])) -> GameInfoDTO:
    game_id = request.cookies.get("game_id")
    if game_id is not None:
        await chess_service.end_game(game_id)

    new_game = await chess_service.init_game(GameInitDTO(first="user"))
    response.set_cookie(
        key = "game_id",
        value = new_game.game_id,
        max_age = 7200,
        path = "/",
    )
    response.status_code = 201
    return new_game

@chess_router.get("/")
@inject
async def get_game_info(game_id: Annotated[str | None, Cookie()] = None, chess_service: ChessService = Depends(Provide[Container.chess_service])) -> GameInfoDTO:
    result = await chess_service.load_game(game_id)
    return result

@chess_router.delete("/")
@inject
async def end_game(game_id: Annotated[str | None, Cookie()] = None, chess_service: ChessService = Depends(Provide[Container.chess_service])) -> str:
    await chess_service.end_game(game_id)
    return f"Game {game_id} was ended, and deleted from db"

@chess_router.get("/history")
@inject
async def get_history(game_id: Annotated[str | None, Cookie()] = None ,chess_service: ChessService = Depends(Provide[Container.chess_service])) -> List[str]:
    return await chess_service.get_history(game_id)

@chess_router.post("/move")
@inject
async def take_a_move(move_dto: MoveDto, game_id: Annotated[str | None, Cookie()] = None, chess_service: ChessService = Depends(Provide[Container.chess_service])) -> TurnResultDTO:
    result = await chess_service.take_a_turn(game_id, move_dto)
    return result

@chess_router.put("/reset")
@inject
async def reset_game(game_id: Annotated[str | None, Cookie()] = None, chess_service: ChessService = Depends(Provide[Container.chess_service])) -> GameInfoDTO:
    result = await chess_service.reset_game(game_id)
    return result.model_dump()