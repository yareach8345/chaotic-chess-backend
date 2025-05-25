from typing import Self

import chess
from chess import Board

from app.domain.chess_game import ChessGame
from app.domain.turn import Turn, MoveResult
from app.dto.move_dto import MoveDto
from app.utils.chess_util import move_unsafe

class AITurn(Turn):
    _board: Board
    captured_piece: chess.Piece | None = None
    def __init__(self, game: ChessGame):
        super().__init__(game.ai_color, game)
        self._board = game.board

    def _generate_next_turn(self) -> Self:
        from app.domain.user_turn import UserTurn
        return UserTurn(self._game)

    def _before_moving(self, move_dto: MoveDto) -> MoveResult:
        if not move_dto.is_piece_symbol_written():
            p = self._board.piece_at(move_dto.get_start_square())
            if p is not None:
                piece = str.upper(p.symbol())
            else:
                piece = "P"
            move_dto.set_piece(piece)
        self.captured_piece = self._board.piece_at(move_dto.get_end_square())
        return MoveResult.ONGOING

    def _moving(self, move_dto: MoveDto) -> MoveResult:
        is_legal_move = True
        piece: chess.Piece | None = None

        if self._board.piece_at(move_dto.get_start_square()) is None or self._game.ai_color != self._board.piece_at(move_dto.get_start_square()).color:
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


        is_legal_move = is_legal_move & move_unsafe(self._board, move_dto)

        if piece is not None:
            self._board.set_piece_at(move_dto.get_start_square(), piece)

        if not is_legal_move:
            move_dto.moving = move_dto.moving + "!"

        return MoveResult.ONGOING

    def _after_moving(self, move_dto: MoveDto) -> MoveResult:
        end_sqare = move_dto.get_end_square()
        piece_symbol_in_end_square = str(self._board.piece_at(end_sqare))
        square_name = chess.square_name(end_sqare)
        ai_promotion_line = 7 if self._game.ai_color else 1
        if piece_symbol_in_end_square.lower() == "p" and square_name.endswith(str(ai_promotion_line)):
            self._board.set_piece_at(end_sqare, chess.Piece.from_symbol("Q" if self._game.ai_color else "q"))
        if self._board.is_checkmate():
            return MoveResult.CHECKMATE_USER_LOSE
        if self.captured_piece is not None and str(self.captured_piece) == ("k" if self._game.ai_color else "K"):
            return MoveResult.USER_LOSE_CUZ_KING_KILLED_BY_AI
        if self.captured_piece is not None and str(self.captured_piece) == ("K" if self._game.ai_color else "k"):
            return MoveResult.AI_PIECE_KILL_AI_KING
        return MoveResult.ONGOING

