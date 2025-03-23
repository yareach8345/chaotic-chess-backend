from typing import List

from pydantic import BaseModel, Field


class ChessMoveDTO(BaseModel):
    moves: List[str]
    new_fen: str