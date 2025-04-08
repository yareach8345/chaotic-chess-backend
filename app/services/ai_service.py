from app.core.ai_client import get_chain, AIResponseAboutMove
from app.dto.ai_request_dto import AIRequestDTO

class AIService:
    _ai_client = get_chain()

    def get_next_move(self, game_info_dto: AIRequestDTO) -> AIResponseAboutMove:
        return self._ai_client.invoke( input = game_info_dto.model_dump() )
