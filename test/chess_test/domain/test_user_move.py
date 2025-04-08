import unittest
from datetime import datetime, timezone

from chess import IllegalMoveError

from app.domain.ai_turn import AITurn
from app.domain.chess_game import ChessGame
from app.domain.turn import generate_turn, MoveResult
from app.dto.move_dto import MoveDto
from app.schemas.chess_game_schema import ChessGameSchema


class TestUserMove(unittest.TestCase):
    sample_data1: ChessGameSchema

    def setUp(self):
        self.sample_data1 = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=[],
            current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w",
            updated_at=datetime.now(timezone.utc)
        )

    def test_user_move(self):
        game = ChessGame(self.sample_data1)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="Nb1a3"))

        self.assertIsInstance(next_turn, AITurn)
        self.assertEqual(game.moves, ["Nb1a3"])
        self.assertEqual(game.turn, False)
        self.assertTrue(game.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/R1BQKBNR b"))

    def test_user_move_but_piece_part_is_wrong(self):
        game = ChessGame(self.sample_data1)
        turn = generate_turn(game)

        with self.assertRaises(IllegalMoveError):
            turn.move(MoveDto(moving="Kb1a2"))

        self.assertEqual(game.moves, [])
        self.assertEqual(game.turn, True)
        self.assertTrue(game.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"))

    def test_user_illegal_move(self):
        game = ChessGame(self.sample_data1)
        turn = generate_turn(game)

        with self.assertRaises(IllegalMoveError):
            turn.move(MoveDto(moving="Nb1a2"))

        self.assertEqual(game.moves, [])
        self.assertEqual(game.turn, True)
        self.assertTrue(game.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"))

    def test_user_try_kill_king(self):
        sample_data2 = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=[],
            current_fen="rnbqkbnr/pppppppp/3N4/8/8/8/PPPPPPPP/R1BQKBNR w",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data2)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="Nd6e8"))

        self.assertEqual(next_turn, MoveResult.USER_LOSE_CUZ_KILL_KING)
        self.assertEqual(game.moves, [])
        self.assertEqual(game.turn, True)
        self.assertTrue(game.board.fen().startswith("rnbqNbnr/pppppppp/8/8/8/8/PPPPPPPP/R1BQKBNR b"))

    def test_user_checkmate(self):
        sample_data2 = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=[],
            current_fen="k6r/8/8/8/8/8/3Q4/1R4K1 w",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data2)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="Qd2a2"))

        self.assertEqual(next_turn, MoveResult.CHECKMATE_USER_WIN)
        self.assertTrue(game.board.fen().startswith("k6r/8/8/8/8/8/Q7/1R4K1 b"))
        self.assertEqual(game.turn, False)


if __name__ == '__main__':
    unittest.main()
