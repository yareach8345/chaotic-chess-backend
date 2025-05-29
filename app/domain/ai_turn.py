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
    # 킹의 위치에서 부터 킹이 아닌 다른 기물이 움직이기 시작할 때 원래 자리에 생성하기 위한 플래그
    needRegenKing: bool = False
    def __init__(self, game: ChessGame):
        super().__init__(game.ai_color, game)
        self._board = game.board

    def _generate_next_turn(self) -> Self:
        from app.domain.user_turn import UserTurn
        return UserTurn(self._game)

    def _before_moving(self, move_dto: MoveDto) -> MoveResult:
        if not move_dto.is_piece_symbol_written():
            #UCI 형식으로 이동할 때, piece를 쓰지 않았을 때
            p = self._board.piece_at(move_dto.get_start_square())
            if p is not None:
                #시작 위치에 기물이 있을 경우
                piece = str.upper(p.symbol())
            else:
                #시작 위치에 기물이 없을 경우 폰으로 설정
                piece = "P"
            move_dto.set_piece(piece)
        piece_at_start = self._board.piece_at(move_dto.get_start_square())

        # 만약 킹이 아닌 다른 기물이 킹의 위치에서 이동하는 경우 킹을 새로 생성하기 위해 플래그를 설정
        if piece_at_start is not None and str(piece_at_start).lower() == 'k' and move_dto.get_piece().piece_type != chess.KING:
            self.needRegenKing = True

        #잡은 기물을 확인
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
        if self.needRegenKing:
            # 킹을 새로 생성
            self._board.set_piece_at(move_dto.get_start_square(), chess.Piece(chess.KING, self._game.ai_color))

        end_sqare = move_dto.get_end_square()
        piece_symbol_in_end_square = str(self._board.piece_at(end_sqare))
        square_name = chess.square_name(end_sqare)
        ai_promotion_line = 7 if self._game.ai_color else 1

        if piece_symbol_in_end_square.lower() == "p" and square_name.endswith(str(ai_promotion_line)):
            #프로모션
            self._board.set_piece_at(end_sqare, chess.Piece.from_symbol("Q" if self._game.ai_color else "q"))
        if self._board.is_checkmate():
            #체크메이트
            return MoveResult.CHECKMATE_USER_LOSE
        if self.captured_piece is not None and str(self.captured_piece) == ("k" if self._game.ai_color else "K"):
            #유저 킹이 AI가 먹힘
            return MoveResult.USER_LOSE_CUZ_KING_KILLED_BY_AI
        if self.captured_piece is not None and str(self.captured_piece) == ("K" if self._game.ai_color else "k"):
            #AI 킹이 AI 기물에게 먹힘
            return MoveResult.AI_PIECE_KILL_AI_KING
        return MoveResult.ONGOING

