from typing import Self

import chess
from chess import Board

from app.domain.chess_game import ChessGame
from app.domain.turn import Turn, MoveResult
from app.dto.move_dto import MoveDto
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
        is_legal_move = True
        piece: chess.Piece | None = None

        if self._game.ai_color != self._board.piece_at(move_dto.get_start_square()).color:
            is_legal_move = False
            piece = self._board.piece_at(move_dto.get_start_square())

            ai_piece = move_dto.get_piece()
            ai_piece.color = self._game.ai_color
            self._board.set_piece_at(move_dto.get_start_square(), ai_piece)
        elif self._board.piece_at(move_dto.get_start_square()).piece_type != move_dto.get_piece().piece_type:
            is_legal_move = False
            ai_piece = move_dto.get_piece()
            ai_piece.color = self._game.ai_color
            self._board.set_piece_at(move_dto.get_start_square(), ai_piece)


        is_legal_move = is_legal_move & ai_move(self._board, move_dto)

        if piece is not None:
            self._board.set_piece_at(move_dto.get_start_square(), piece)

        if not is_legal_move:
            move_dto.moving = move_dto.moving + "!"

        return MoveResult.ONGOING

    def _after_moving(self, move_dto: MoveDto) -> MoveResult:
        if self._board.is_checkmate():
            return MoveResult.CHECKMATE_USER_LOSE
        return MoveResult.ONGOING

