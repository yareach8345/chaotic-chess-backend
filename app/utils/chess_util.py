import chess
from chess import Board, Move, Piece, Square, parse_square

from app.dto.move_dto import MoveDto


# 새로운 게임을 생성
# 게임 초기 상태를 반환
def init_game() -> Board:
    return Board()

# 기존 진행중이던 게임의 fen 표기를 Board로 변환
def fen_to_board(fen: str) -> Board:
    return Board(fen)

# 유저의 움직임을 수행
# push_uci 메서드를 이용하여 "합법적인" 움직임만 강제
def user_move(board: Board, move: MoveDto) -> bool:
    board.push_uci(move.to_uci())
    return True

def ai_move(board: Board, move: MoveDto) -> bool:
    try:
        board.push_uci(move.to_uci())
        return True
    except chess.IllegalMoveError:
        board.push(Move.from_uci(move.to_uci()))
        return False