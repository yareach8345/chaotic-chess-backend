import re
from typing import Any

import chess
from pydantic import BaseModel, Field

chess_moving_regex = re.compile(r"(?P<piece>[PRNBKQ])?(?P<start>[a-h][1-8])(?P<x>x)?(?P<end>[a-h][1-8])(?P<promotion>[rnbqRNBQ])?(?P<check>[+#])?")

class MoveDto(BaseModel):
    moving: str

    def set_piece(self, piece: str):
        if self.is_piece_symbol_written():
            self.moving = piece + self.moving[1:]
        else:
            self.moving = piece + self.moving

    def can_parsing(self) -> bool:
        return chess_moving_regex.match(self.moving) is not None

    def to_uci(self):
        match = chess_moving_regex.match(self.moving)
        return f"{match.group("start")}{match.group("end")}{match.group("promotion") if match.group("promotion") else ""}"

    def is_piece_symbol_written(self):
        match = chess_moving_regex.match(self.moving)
        return match.group("piece") is not None

    def get_piece(self):
        match = chess_moving_regex.match(self.moving)
        if match.group("piece") is None:
            return chess.Piece.from_symbol("P")
        else:
            return chess.Piece.from_symbol(self.moving[0])

    def get_start_square(self):
        match = chess_moving_regex.match(self.moving)
        return chess.parse_square(match.group("start"))

    def get_end_square(self):
        match = chess_moving_regex.match(self.moving)
        return chess.parse_square(match.group("end"))
