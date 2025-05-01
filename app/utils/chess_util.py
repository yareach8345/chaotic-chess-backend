from typing import List

import asyncio
import chess
from chess import Board, Move, Piece, Square, parse_square, square_name

from app.dto.PieceInfo import PieceInfo, PieceMap
from app.dto.move_dto import MoveDto


# 새로운 게임을 생성
# 게임 초기 상태를 반환
def init_game() -> Board:
    return Board()

# 기존 진행중이던 게임의 fen 표기를 Board로 변환
def fen_to_board(fen: str) -> Board:
    return Board(fen)

def get_movable_cells(fen: str, square: str) -> List[str]:
    board = Board(fen)
    legal_moves = [square_name(move.to_square) for move in board.legal_moves if move.from_square == parse_square(square)]
    return legal_moves

async def get_piece_info_from_fen(fen: str) -> List[PieceInfo]:
    def do():
        piece_map_items = Board(fen).piece_map().items()
        result = []
        for square_num, piece in piece_map_items:
            square = square_name(square_num)
            new_piece_info = PieceInfo(
                square=square,
                color="w" if piece.color else "b",
                type=piece.symbol().lower(),
                movable=get_movable_cells(fen, square)
            )
            result.append(new_piece_info)
        return result
    return await asyncio.to_thread(do)


# 유저의 움직임을 수행
# push_uci 메서드를 이용하여 "합법적인" 움직임만 강제
def move(board: Board, move_dto: MoveDto) -> bool:
    board.push_uci(move_dto.to_uci())
    return True

def move_unsafe(board: Board, move_dto: MoveDto) -> bool:
    try:
        board.push_uci(move_dto.to_uci())
        return True
    except chess.IllegalMoveError:
        board.push(Move.from_uci(move_dto.to_uci()))
        return False