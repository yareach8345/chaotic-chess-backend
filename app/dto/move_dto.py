import enum

from chess import Piece
from pydantic import BaseModel, Field


class PieceType(enum.Enum):
    PAWN = "p"
    KNIGHT = "n"
    QUEEN = "q"
    KING = "k"
    ROOK = "r"
    BISHOP = "b"

class PieceColor(enum.Enum):
    WHITE = "white"
    BLACK = "black"

class MoveDto(BaseModel):
    color: PieceColor
    piece: PieceType
    start: str | None = Field(default=None)
    end: str

    def to_uci(self) -> str:
        if self.start is None:
            _start_part = "??"
        else:
            _start_part = self.start
        return f"{_start_part}{self.end}"

    def to_piece(self) -> Piece:
        if self.color == PieceColor.WHITE:
            # 화이트일 경우 대문자로 변환.
            return Piece.from_symbol(str.upper(self.piece.value))
        else:
            # 블랙일 경우 소문자로 변환
            return Piece.from_symbol(str.lower(self.piece.value))

    def to_algebraic(self):
        if self.piece == PieceType.PAWN:
            part_of_piece = ""
        else:
            part_of_piece = str.upper(self.piece.value)

        return f"{part_of_piece}{self.to_uci()}"

class UserMoveDto(MoveDto):
    pass

class AIMoveType(enum.Enum):
    GEN = "gen"
    MOV = "mov"

class AIMoveDto(MoveDto):
    type: AIMoveType

    def to_uci(self) -> str:
        if self.start is None or self.type == AIMoveType.GEN:
            _start_part = "??"
        else:
            _start_part = self.start
        return f"{_start_part}{self.end}"
