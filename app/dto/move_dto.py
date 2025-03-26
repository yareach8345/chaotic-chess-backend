import enum

from chess import Piece
from pydantic import BaseModel, Field


class PieceType(enum.Enum):
    PAWN = "p"
    KNIGHT = "k"
    QUEEN = "q"
    KING = "k"
    ROOK = "r"
    BISHOP = "b"

class PieceColor(enum.Enum):
    WHITE = "white"
    BLACK = "black"

class _MoveDto(BaseModel):
    color: PieceColor
    piece: PieceType
    start: str | None = Field(default=None)
    end: str

    def to_uci(self) -> str:
        return f"{self.start}{self.end}"

    def to_piece(self) -> Piece:
        if self.color == PieceColor.WHITE:
            # 화이트일 경우 대문자로 변환.
            return Piece.from_symbol(str.upper(self.piece.value))
        else:
            # 블랙일 경우 소문자로 변환
            return Piece.from_symbol(str.lower(self.piece.value))

class UserMoveDto(_MoveDto):
    pass

class AIMoveType(enum.Enum):
    GEN = "gen"
    MOV = "mov"

class AIMoveDto(_MoveDto):
    type: AIMoveType
