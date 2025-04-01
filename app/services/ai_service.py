from app.core.ai_client import get_chain, AIResponseAboutMove
from app.dto.game_info_dto import GameInfoDTO

class AIService:
    _ai_client = get_chain()

    def get_next_move(self, game_info_dto: GameInfoDTO) -> AIResponseAboutMove:
        return self._ai_client.invoke( input = game_info_dto.model_dump() )
