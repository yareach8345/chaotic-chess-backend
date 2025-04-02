import chess
from pydantic import BaseModel, Field

class MoveDto(BaseModel):
    fen: str

    def to_uci(self):
        return self.fen[1:5]

    def get_piece(self):
        return chess.Piece.from_symbol(self.fen[0])

    def get_start_square(self):
        return chess.parse_square(self.fen[1:3])

    def get_end_square(self):
        return chess.parse_square(self.fen[3:5])
