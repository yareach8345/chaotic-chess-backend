import unittest

from app.dto.ai_request_dto import AIRequestDTO
from app.services.ai_service import AIService


class AIServiceTest(unittest.TestCase):
    _ai_service = AIService()

    def test_ai_service(self):
        result = self._ai_service.get_next_move(AIRequestDTO(
            moves=[],
            user_move="Pd2d4",
            ai_role="black",
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
        ))
        print(result)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
