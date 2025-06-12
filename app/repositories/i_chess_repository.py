import abc

from app.domain.turn import MoveResult
from app.dto.db_update_dto import DBUpdateWithMovingDto
from app.schemas.chess_game_schema import ChessGameSchema


class IChessRepository(metaclass=abc.ABCMeta):
    async def save(self, chess_game_schema: ChessGameSchema) -> str:
        pass

    async def get_by_id(self, chess_game_id: str) -> ChessGameSchema | None:
        pass

    async def update_by_moving(self, chess_game_id: str, chess_move_dto: DBUpdateWithMovingDto):
        pass

    async def delete_data(self, chess_game_id: str):
        pass

    async def end_game(self, chess_game_id: str, result: MoveResult):
        pass

    async def reset_game(self, chess_game_id: str):
        pass

    async def check_game_is_exist(self, chess_game_id: str) -> bool:
        pass