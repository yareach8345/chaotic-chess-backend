from typing import List, Final

from chess import Board

from app.dto.move_dto import MoveDto
from app.schemas.chess_game_schema import ChessGameSchema
from app.utils.chess_util import fen_to_board, move, move_unsafe

class ChessGame:
    """
    채스 게임의 상태를 저장하는 클래스

    맴버변수:
        board (Board): 현재 게임의 보드 상태를 저장, 게임을 진행하는데 필요한 Board 객체
        moves (List[str]): 게임의 시작부터 현재까지의 움직임의 결과를 담는 배열
        user_color (Final[bool]): user의 말의 색깔을 기록
        ai_color (Final[bool]): ai의 말의 색깔을 기록
        turn (bool): 혀재 누구의 턴인지 기록한다. turn에 저장된 값과 동일한 값을 가지고 있는 쪽의 차례이다.
    """
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
        """
        move정보를 받아 moves를 업데이트 합니다.

        Args:
            move (MoveDto): 업데이트 할 move
        """
        self.turn = not self.turn
        self.moves.append(move.moving)