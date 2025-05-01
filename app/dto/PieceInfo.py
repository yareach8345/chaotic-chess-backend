from typing import List

from pydantic import BaseModel

class PieceInfo(BaseModel):
    square: str
    type: str
    color: str
    movable: List[str] | None

type PieceMap = list[list[PieceInfo | None]]