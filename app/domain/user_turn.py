from typing import Self

from chess import Board, Square, parse_square, IllegalMoveError

from app.domain.chess_game import ChessGame
from app.domain.turn import Turn, MoveResult
from app.dto.move_dto import MoveDto
from app.utils.chess_util import move, move_unsafe


class UserTurn(Turn):
    _board: Board

    def __init__(self, game: ChessGame):
        super().__init__(game.user_color, game)
        self._board = game.board

    def _before_moving(self, move_dto: MoveDto) -> MoveResult:
        piece = self._board.piece_at(move_dto.get_start_square())
        if piece.piece_type != move_dto.get_piece().piece_type or piece.color != self._game.user_color:
            raise IllegalMoveError(f"Fen is {move_dto.moving}. But a piece in the cell '{move_dto.get_start_square()}' is ${move_dto.get_piece()}")

        return MoveResult.ONGOING

    def _moving(self, move_dto: MoveDto) -> MoveResult:
        piece_at_end = self._board.piece_at(move_dto.get_end_square())

        # 6 is king
        # 유저가 할 수 있는 유일한 unsafe한 이동 왕을 먹는것. 하지만 이후 유저는 패배한다.
        if piece_at_end is not None and piece_at_end.piece_type == 6:
            move_unsafe(self._board, move_dto)
            return MoveResult.USER_LOSE_CUZ_KILL_KING

        move(self._board, move_dto)

        return MoveResult.ONGOING

    def _after_moving(self, move_dto: MoveDto) -> MoveResult:
        if self._board.is_checkmate():
            return MoveResult.CHECKMATE_USER_WIN
        return MoveResult.ONGOING

    def _generate_next_turn(self) -> Self:
        from app.domain.ai_turn import AITurn
        return AITurn(self._game)