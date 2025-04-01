from typing import List

from pydantic import BaseModel

class GameInfoDTO(BaseModel):
    moves: List[str]
    user_move: str | None
    ai_role: str
    fen: str
