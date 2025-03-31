import unittest
from datetime import datetime, timezone

from app.domain.ai_turn import AITurn
from app.domain.chess_game import ChessGame
from app.domain.turn import generate_turn
from app.domain.user_turn import UserTurn
from app.schemas.chess_game_schema import ChessGameSchema


class TestTurn(unittest.TestCase):
    sample_data1 = ChessGameSchema(
        game_status="ongoing",
        white="ai",
        moves=[],
        current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w",
        updated_at=datetime.now(timezone.utc)
    )

    sample_data2 = ChessGameSchema(
        game_status="ongoing",
        white="user",
        moves=[],
        current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w",
        updated_at=datetime.now(timezone.utc)
    )

    def test_generate_turn(self):
        game = ChessGame(self.sample_data1)
        turn = generate_turn(game)
        self.assertIsInstance(turn, AITurn)

        game = ChessGame(self.sample_data2)
        turn = generate_turn(game)
        self.assertIsInstance(turn, UserTurn)

    def test_generate_next_turn(self):
        game = ChessGame(self.sample_data1)
        first_turn = generate_turn(game)
        second_turn = first_turn._generate_next_turn()
        third_turn = second_turn._generate_next_turn()

        self.assertIsInstance(first_turn, AITurn)
        self.assertIsInstance(second_turn, UserTurn)
        self.assertIsInstance(third_turn, AITurn)
