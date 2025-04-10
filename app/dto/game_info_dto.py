from typing import List

from pydantic import BaseModel

from app.schemas.chess_game_schema import ChessGameSchema


class GameInfoDTO(BaseModel):
    game_id: str | None
    moves: List[str]
    white: str
    fen: str
    game_status: str

    def to_chess_game_schema(self) -> ChessGameSchema:
        return ChessGameSchema(
            _id=self.game_id,
            game_status = self.game_status,
            white = self.white,
            moves = self.moves,
            current_fen= self.fen,
        )

def from_chess_game_schema(chess_game_schema: ChessGameSchema) -> GameInfoDTO:
    return GameInfoDTO(
        game_id=chess_game_schema.id,
        moves=chess_game_schema.moves,
        white=chess_game_schema.white,
        fen=chess_game_schema.current_fen,
        game_status=chess_game_schema.game_status,
    )