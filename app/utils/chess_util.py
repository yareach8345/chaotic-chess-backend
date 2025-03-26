import chess
from chess import Board, Move, Piece, Square, parse_square

from app.dto.move_dto import UserMoveDto, AIMoveDto, AIMoveType, PieceColor, PieceType

# 새로운 게임을 생성
# 게임 초기 상태를 반환
def init_game() -> Board:
    return Board()

# 기존 진행중이던 게임의 fen 표기를 Board로 변환
def fen_to_board(fen: str) -> Board:
    return Board(fen)

# 유저의 움직임을 수행
# push_uci 메서드를 이용하여 "합법적인" 움직임만 강제
def user_move(board: Board, move_dto: UserMoveDto):
    board.push_uci(move_dto.to_uci())

# dto의 end필드에 명시된 위치에 piece에 해당하는 기물을 소환
# 절대로 합법적인 움직임이 될 수 없으므로 ai의 움직임에만 사용할 것
def generate_piece(board: Board, move_dto: AIMoveDto):
    # 생성되 위치(end)를 square타입으로 변환
    generated_at = parse_square(move_dto.end)

    # 기물이 생성될 위치에 기물이 있을 시 해당 기물을 잡힌 것으로 처리하기 위한 플러그
    is_capture = board.piece_at(generated_at) is not None

    # 피스를 소환
    board.set_piece_at(generated_at, move_dto.to_piece())

    # 턴이 지남을 처리하는 로직
    # 턴을 상대의 턴으로 설정하고, 흑의 차례일 때 fullmove_number를 증가시킴
    # 해당 위치에 본래 기물이 있었을 경우 혹은 소환된 기물이 폰일 경우(폰이 움직인 해석) 카운트를 초기화
    board.turn = not board.turn

    if board.turn == chess.BLACK:
        board.fullmove_number += 1

    if is_capture or move_dto.piece == PieceType.PAWN:
        board.halfmove_clock = 0
    else:
        board.halfmove_clock += 1


# ai의 움직임을 수행
# type이 GEN일 경우 기물을 생성
# type이 MOV일 경우 기물을 이동
# MOV의 경우 합법적인 움직임인지 검사하지 않음
def ai_move(board: Board, move_dto: AIMoveDto):
    if move_dto.type == AIMoveType.GEN:
        generate_piece(board, move_dto)
    else:
        board.push(Move.from_uci(move_dto.to_uci()))