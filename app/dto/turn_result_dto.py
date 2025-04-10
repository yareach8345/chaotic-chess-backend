from pydantic import BaseModel

from app.domain.turn import MoveResult
from app.dto.game_info_dto import GameInfoDTO


class TurnResultDTO(BaseModel):
    game_info: GameInfoDTO
    move_result: MoveResult
    moves_in_this_turn: list[str]
    ai_saying: str | None