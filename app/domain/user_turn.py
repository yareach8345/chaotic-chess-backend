from typing import Self

from chess import Board, Square, parse_square, IllegalMoveError

from app.domain.chess_game import ChessGame
from app.domain.turn import Turn, MoveResult
from app.dto.move_dto import MoveDto
from app.utils.chess_util import user_move

class UserTurn(Turn):
    _board: Board

    def __init__(self, game: ChessGame):
        super().__init__(game.user_color, game)
        self._board = game.board

    def _before_moving(self, move: MoveDto) -> MoveResult:
        piece = self._board.piece_at(move.get_start_square())
        if piece.piece_type != move.get_piece().piece_type or piece.color != self._game.user_color:
            raise IllegalMoveError(f"Fen is {move.moving}. But a piece in the cell '{move.get_start_square()}' is ${move.get_piece()}")

        return MoveResult.ONGOING

    def _moving(self, move: MoveDto) -> MoveResult:
        piece_at_end = self._board.piece_at(move.get_end_square())

        user_move(self._board, move)

        # 6 is king
        if piece_at_end is not None and piece_at_end.piece_type == 6:
            return MoveResult.USER_LOSE_CUZ_KILL_KING

        return MoveResult.ONGOING

    def _after_moving(self, move: MoveDto) -> MoveResult:
        if self._board.is_checkmate():
            return MoveResult.CHECKMATE_USER_WIN
        return MoveResult.ONGOING

    def _generate_next_turn(self) -> Self:
        from app.domain.ai_turn import AITurn
        return AITurn(self._game)