from typing import Self

from chess import Board, Square, parse_square

from app.domain.chess_game import ChessGame
from app.domain.turn import Turn, MoveResult
from app.dto.move_dto import MoveDto, UserMoveDto
from app.utils.chess_util import user_move

class UserTurn(Turn):
    _board: Board

    def __init__(self, game: ChessGame):
        super().__init__(game.user_color, game)
        self._board = game.board

    def _generate_next_turn(self) -> Self:
        from app.domain.ai_turn import AITurn
        return AITurn(self._game)

    def _after_moving(self, move_dto: MoveDto):
        if self._board.is_checkmate():
            return MoveResult.CHECKMATE_USER_WIN
        return MoveResult.ONGOING

    def _moving(self, move_dto: MoveDto):
        piece_at_end = self._board.piece_at(parse_square(move_dto.end))

        if not isinstance(move_dto, UserMoveDto):
            return MoveResult.ILLEGAL_INPUT

        try:
            user_move(self._board, move_dto)
        except Exception as e:
            return MoveResult.ILLEGAL_INPUT

        # 6 is king
        if piece_at_end is not None and piece_at_end.piece_type == 6:
            return MoveResult.USER_LOSE_CUZ_KILL_KING

        return MoveResult.ONGOING

    def _before_moving(self, move_dto: MoveDto):
        return MoveResult.ONGOING