from typing import List, Final

from chess import Board

from app.dto.move_dto import MoveDto
from app.schemas.chess_game_schema import ChessGameSchema
from app.utils.chess_util import fen_to_board, user_move, ai_move

class ChessGame:

    board: Board

    #현재턴까지의 이동 기록
    moves: List[str]

    #유저와 ai의 턴을 bool로 저장한다.
    #True는 white를 False는 black을 의미한다.
    user_color: Final[bool]
    ai_color: Final[bool]

    turn: bool

    def __init__(self, chess_game_schema: ChessGameSchema):
        self.board = fen_to_board(chess_game_schema.current_fen)
        self.moves = chess_game_schema.moves
        self.user_color = chess_game_schema.white == "user"
        self.ai_color = chess_game_schema.white == "ai"
        #이동 수의 나머지가 0이라면 짝수번 이동한 상태 -> 백(True)의 차례
        #이동 수의 나머지가 0이 아니라면 반대로 흑(False)의 차례
        self.turn = True if len(self.moves) % 2 == 0 else False

    def after_turn(self, move: MoveDto):
        self.turn = not self.turn
        self.moves.append(move.fen)