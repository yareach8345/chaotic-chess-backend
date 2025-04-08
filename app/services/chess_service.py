from typing import List

from app.domain.chess_game import ChessGame
from app.domain.turn import generate_turn
from app.dto.ai_request_dto import AIRequestDTO
from app.dto.game_info_dto import GameInfoDTO, from_chess_game_schema
from app.dto.game_init_dto import GameInitDTO
from app.dto.move_dto import MoveDto
from app.repositories.i_chess_repository import IChessRepository
from app.schemas.chess_game_schema import ChessGameSchema
from app.services.ai_service import AIService

from app.services.i_chess_service import IChessService
from app.utils.chess_util import init_game


class ChessService(IChessService):
    _repository: IChessRepository
    _ai_service: AIService

    def __init__(self, repository: IChessRepository, ai_service: AIService):
        self._repository = repository
        self._ai_service = ai_service

    async def init_game(self, game_info_dto: GameInitDTO) -> GameInfoDTO:
        b = init_game()

        new_game_schema = ChessGameSchema(
            game_status="ongoing",
            white=game_info_dto.first,
            moves=[],
            current_fen=b.fen(),
        )

        new_game_id = await self._repository.save(new_game_schema)
        result = from_chess_game_schema(new_game_schema)
        result.game_id = new_game_id
        return result

    async def load_game(self, game_id: str) -> GameInfoDTO | None:
        schema = await self._repository.get_by_id(game_id)
        if schema is not None:
            return from_chess_game_schema(schema)
        else:
            return None

    async def take_a_move(self, game_id: str, user_move: MoveDto) -> GameInfoDTO:
        chess_game = ChessGame(await self._repository.get_by_id(game_id))
        user_turn = generate_turn(chess_game)
        ai_turn = user_turn.move(user_move)
        ai_moving = self._ai_service.get_next_move(
            AIRequestDTO(
                moves = chess_game.moves,
                user_move = user_move.to_uci(),
                ai_role= "white" if chess_game.ai_color == True else "black",
                fen = chess_game.board.fen()
            )
        )
        ai_turn.move(MoveDto(
            moving= ai_moving.ai_moving
        ))
        result = GameInfoDTO(
            game_id = game_id,
            moves = chess_game.moves,
            white = "ai" if chess_game.ai_color == True else "user",
            fen = chess_game.board.fen()
        )
        await self._repository.save(result.to_chess_game_schema())
        return result

    async def get_history(self, game_id: str) -> List[str]:
        return (await self._repository.get_by_id(game_id)).moves

    async def end_game(self, game_id: str):
        await self._repository.end_game(game_id)

    async def reset_game(self, game_id: str):
        await self._repository.reset_game(game_id)
