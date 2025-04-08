from typing import List

from pydantic import BaseModel

class AIRequestDTO(BaseModel):
    """
    AI에 다음 수의 request로 보낼 때 사용할 DTO객체
    """
    moves: List[str]
    user_move: str | None
    ai_role: str
    fen: str