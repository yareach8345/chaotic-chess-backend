from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field
from uuid import UUID

class ChessGameSchema(BaseModel):
    id: UUID | None = Field(default=None)
    game_status: str
    white: str
    moves: List[str]
    current_fen: str
    updated_at: datetime = Field(default_factory = lambda data: datetime.now(timezone.utc))