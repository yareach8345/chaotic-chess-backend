import unittest
from datetime import datetime, timezone
from random import sample
from typing import Self

from app.domain.chess_game import ChessGame
from app.domain.turn import Turn, MoveResult
from app.dto.move_dto import MoveDto
from app.exception.game_exception import GameException
from app.schemas.chess_game_schema import ChessGameSchema


class ChessGameTest(unittest.TestCase):
    sample_data1: ChessGameSchema
    sample_data2: ChessGameSchema

    def setUp(self):
        self.sample_data1 = ChessGameSchema(
            game_status="ongoing",
            white="ai",
            moves=[],
            current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w",
            updated_at=datetime.now(timezone.utc)
        )

        self.sample_data2 = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=["a2a4"],
            current_fen="rnbqkbnr/pppppppp/8/8/1P6/8/P1PPPPPP/RNBQKBNR w",
            updated_at=datetime.now(timezone.utc)
        )

    def test_generate(self):
        game = ChessGame(self.sample_data1)
        self.assertEqual(game.user_color, False)
        self.assertEqual(game.ai_color, True)
        self.assertEqual(game.turn, True)

        game = ChessGame(self.sample_data2)
        self.assertEqual(game.user_color, True)
        self.assertEqual(game.ai_color, False)
        self.assertEqual(game.turn, False)

    def test_after_move(self):
        game = ChessGame(self.sample_data1)
        first_bool = game.turn
        game.after_turn(MoveDto(moving="FEN"))
        self.assertEqual(not first_bool, game.turn)
        self.assertEqual(game.moves, ["FEN"])