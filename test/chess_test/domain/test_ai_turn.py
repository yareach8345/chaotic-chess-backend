import unittest
from datetime import datetime, timezone

from app.domain.chess_game import ChessGame
from app.domain.turn import generate_turn, MoveResult
from app.domain.user_turn import UserTurn
from app.dto.move_dto import MoveDto
from app.schemas.chess_game_schema import ChessGameSchema


class TestAIMove(unittest.TestCase):
    sample_data1: ChessGameSchema

    def setUp(self):
        self.sample_data1 = ChessGameSchema(
        game_status="ongoing",
        white="ai",
        moves=[],
        current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w",
        updated_at=datetime.now(timezone.utc)
    )

    def test_ai_move(self):
        game = ChessGame(self.sample_data1)
        turn = generate_turn(game)
        next_turn = turn.move( MoveDto(fen="Nb1a3") )

        self.assertIsInstance(next_turn, UserTurn)
        self.assertEqual(game.moves, ["Nb1a3"])
        self.assertEqual(game.turn, False)
        self.assertTrue(game.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/R1BQKBNR b"))

    def test_user_illegal_move_but_illegal_move_not_except(self):
        game = ChessGame(self.sample_data1)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(fen="Nb1a2"))

        self.assertIsInstance(next_turn, UserTurn)
        self.assertEqual(game.moves, ["Nb1a2!"])
        self.assertEqual(game.turn, False)
        self.assertTrue(game.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/8/NPPPPPPP/R1BQKBNR b"))

    def test_ai_checkmate(self):
        sample_data2 = ChessGameSchema(
            game_status="ongoing",
            white="ai",
            moves=[],
            current_fen="k6r/8/8/8/8/8/3Q4/1R4K1 w",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data2)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(fen="Qd2a2"))

        self.assertEqual(next_turn, MoveResult.CHECKMATE_USER_LOSE)
        self.assertTrue(game.board.fen().startswith("k6r/8/8/8/8/8/Q7/1R4K1 b"))
        self.assertEqual(game.turn, False)

    def test_change_piece_when_ai_trying_other_piece_then_on_the_start_cell(self):
        sample_data2 = ChessGameSchema(
            game_status="ongoing",
            white="ai",
            moves=[],
            current_fen="k6r/8/8/8/8/8/3Q4/1R4K1 w",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data2)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(fen="Nd2a2"))

        self.assertNotEqual(next_turn, MoveResult.CHECKMATE_USER_LOSE)
        self.assertIsInstance(next_turn, UserTurn)
        self.assertTrue(game.board.fen().startswith("k6r/8/8/8/8/8/N7/1R4K1 b"))
        self.assertEqual(game.turn, False)

    def test_generate_a_piece_when_there_is_a_other_color_piece_on_the_start_cell(self):
        sample_data2 = ChessGameSchema(
            game_status="ongoing",
            white="ai",
            moves=[],
            current_fen="k6r/8/8/8/8/8/3Q4/1R4K1 w",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data2)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(fen="Na8b6"))

        self.assertIsInstance(next_turn, UserTurn)
        self.assertTrue(game.board.fen().startswith("k6r/8/1N6/8/8/8/3Q4/1R4K1 b"))
        self.assertEqual(game.turn, False)


if __name__ == '__main__':
    unittest.main()
