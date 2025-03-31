from typing import Self

from chess import Board

from app.domain.chess_game import ChessGame
from app.domain.turn import Turn, MoveResult
from app.dto.move_dto import MoveDto, AIMoveDto
from app.utils.chess_util import ai_move

class AITurn(Turn):
    _board: Board
    def __init__(self, game: ChessGame):
        super().__init__(game.ai_color, game)
        self._board = game.board

    def _generate_next_turn(self) -> Self:
        from app.domain.user_turn import UserTurn
        return UserTurn(self._game)

    def _before_moving(self, move_dto: MoveDto) -> MoveResult:
        return MoveResult.ONGOING

    def _moving(self, move_dto: MoveDto) -> MoveResult:
        if not isinstance(move_dto, AIMoveDto):
            return MoveResult.ILLEGAL_INPUT

        try:
            ai_move(self._board, move_dto)
        except Exception as e:
            return MoveResult.ILLEGAL_INPUT

        return MoveResult.ONGOING

    def _after_moving(self, move_dto: MoveDto) -> MoveResult:
        if self._board.is_checkmate():
            return MoveResult.CHECKMATE_USER_LOSE
        return MoveResult.ONGOING

