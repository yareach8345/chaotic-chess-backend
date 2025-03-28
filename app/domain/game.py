from typing import List, Final

from chess import Board

from app.dto.move_dto import UserMoveDto, AIMoveDto, MoveDto
from app.exception.game_exception import GameException
from app.schemas.chess_game_schema import ChessGameSchema
from app.utils.chess_util import fen_to_board, user_move, ai_move

## todo: write test codes

class Game:
    board: Board
    #현제 차례가 누구 차례인가
    #True는 백의 차례임을, False는 흑의 차럐임을 의미한다.
    _turn: bool
    #user와 ai가 어떤 색의 기물을 움직이는지를 담는다.
    #_turn과 마찬가지로 true는 백이고, false는 흑이다
    #한쪽은 백, 한쪽은 흑이어야 하므로 _user_role와 _ai_role의 xor 연산 결과는 항상 true여야 한다.
    _user_role: Final[bool]
    _ai_role: Final[bool]

    #현재턴까지의 이동 기록
    moves: List[str]

    def __init__(self, chess_game_schema: ChessGameSchema):
        self.board = fen_to_board(chess_game_schema.current_board)
        self._turn = self.board.turn
        self._user_role = chess_game_schema.white == 'user'
        self._ai_role = self._user_role ^ True
        self.moves = chess_game_schema.moves

    def _user_move(self, move_dto: UserMoveDto):
        # 해당 턴이 유저의 턴이 아닐 경우 에러 발생
        if self._user_role != self._turn:
            raise GameException("It's not users turn. but user try move")
        user_move(self.board, move_dto)

    def _ai_move(self, move_dto: AIMoveDto):
        # 해당 턴이 ai의 턴이 아닐 경우 에러 발생
        if self._ai_role != self._turn:
            raise GameException("It's not ai turn. but ai try move")
        ai_move(self.board, move_dto)

    def move(self, move_dto: MoveDto):
        if isinstance(move_dto, UserMoveDto):
            self._user_move(move_dto)
        elif isinstance(move_dto, AIMoveDto):
            self._ai_move(move_dto)
        else:
            raise GameException("Who try moving now?")
        self.moves.append(move_dto.to_algebraic())
