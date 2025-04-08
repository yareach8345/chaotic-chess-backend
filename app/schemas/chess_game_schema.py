from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field

class ChessGameSchema(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    game_status: str
    white: str
    moves: List[str]
    current_fen: str
    updated_at: datetime = Field(default_factory = lambda data: datetime.now(timezone.utc))