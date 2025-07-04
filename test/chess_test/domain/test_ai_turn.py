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
        next_turn = turn.move(MoveDto(moving="Nb1a3"))

        self.assertIsInstance(next_turn, UserTurn)
        self.assertEqual(game.moves, ["Nb1a3"])
        self.assertEqual(game.turn, False)
        self.assertTrue(game.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/R1BQKBNR b"))

    def test_user_illegal_move_but_illegal_move_not_except(self):
        game = ChessGame(self.sample_data1)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="Nb1a2"))

        self.assertIsInstance(next_turn, UserTurn)
        self.assertEqual(game.moves, ["Nb1a2!"])
        self.assertEqual(game.turn, False)
        self.assertTrue(game.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/8/NPPPPPPP/R1BQKBNR b"))

    def test_ai_promotion(self):
        sample_data = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=["Pd2d1"],
            current_fen="k6r/8/8/8/8/8/3p4/1R4K1 b",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="Pd2d1"))
        self.assertIsInstance(next_turn, UserTurn)
        self.assertTrue(game.board.fen().startswith("k6r/8/8/8/8/8/8/1R1q2K1 w"))

    def test_ai_try_users_king(self):
        sample_data = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=["Pd2d1"],
            current_fen="k6r/8/8/8/8/8/5p2/1R4K1 b",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="Pf2g1"))
        self.assertEqual(next_turn, MoveResult.USER_LOSE_CUZ_KING_KILLED_BY_AI)
        self.assertTrue(game.board.fen().startswith("k6r/8/8/8/8/8/8/1R4q1 w"))

    def test_ai_try_users_king2(self):
        sample_data = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=["kc5d1"],
            current_fen="k6r/8/8/8/8/8/5p2/1R4K1 b",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="Kc5g1"))
        self.assertEqual(next_turn, MoveResult.USER_LOSE_CUZ_KING_KILLED_BY_AI)
        print(game.board.fen())
        self.assertTrue(game.board.fen().startswith("k6r/8/8/8/8/8/5p2/1R4k1 w"))


    def test_ai_try_selves_king(self):
        sample_data = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=["Pd2d1"],
            current_fen="k6r/8/8/8/8/8/5p2/1R4K1 b",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="h8a8"))
        self.assertEqual(next_turn, MoveResult.AI_PIECE_KILL_AI_KING)
        self.assertTrue(game.board.fen().startswith("r7/8/8/8/8/8/5p2/1R4K1 w"))

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
        next_turn = turn.move(MoveDto(moving="Qd2a2"))

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
        next_turn = turn.move(MoveDto(moving="Nd2a2"))

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
        next_turn = turn.move(MoveDto(moving="Na8b6"))

        self.assertIsInstance(next_turn, UserTurn)
        self.assertTrue(game.board.fen().startswith("k6r/8/1N6/8/8/8/3Q4/1R4K1 b"))
        self.assertEqual(game.turn, False)

    def test_regen_white_king(self):
        sample_data2 = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=["Kg1h1"],
            current_fen="k7/8/8/8/8/8/8/7K b",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data2)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="Qh1g2"))
        self.assertIsInstance(next_turn, UserTurn)
        self.assertTrue(game.board.fen().startswith("k7/8/8/8/8/8/6q1/7K w"))

    def test_regen_black_king(self):
        sample_data2 = ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=["Kg1h1"],
            current_fen="k7/8/8/8/8/8/8/7K b",
            updated_at=datetime.now(timezone.utc)
        )
        game = ChessGame(sample_data2)
        turn = generate_turn(game)
        next_turn = turn.move(MoveDto(moving="Qa8g2"))
        self.assertIsInstance(next_turn, UserTurn)
        self.assertTrue(game.board.fen().startswith("k7/8/8/8/8/8/6q1/7K w"))

if __name__ == '__main__':
    unittest.main()
