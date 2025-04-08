import chess
from pydantic import BaseModel, Field

class MoveDto(BaseModel):
    moving: str

    def to_uci(self):
        if len(self.moving) == 4:
            return self.moving
        else:
            return self.moving[1:5]

    def get_piece(self):
        if len(self.moving) == 4:
            return chess.Piece.from_symbol("P")
        else:
            return chess.Piece.from_symbol(self.moving[0])

    def get_start_square(self):
        if len(self.moving) == 4:
            return chess.parse_square(self.moving[0:2])
        else:
            return chess.parse_square(self.moving[1:3])

    def get_end_square(self):
        if len(self.moving) == 4:
            return chess.parse_square(self.moving[2:4])
        else:
            return chess.parse_square(self.moving[3:5])
