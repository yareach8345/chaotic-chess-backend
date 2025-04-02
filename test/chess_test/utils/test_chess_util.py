import unittest

from chess import IllegalMoveError

from app.dto.move_dto import MoveDto
from app.utils.chess_util import init_game, user_move, ai_move, fen_to_board


class ChessUtilTest(unittest.TestCase):
    def test_generate_game(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
        initialized_game = init_game()
        self.assertTrue(initialized_game.fen().startswith(fen))

    def test_generate_from_fen(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
        initialized_game = fen_to_board(fen)
        self.assertTrue(initialized_game.fen().startswith(fen))

    def test_user_move(self):
        fen = "r1bqkbnr/pppppppp/n7/8/8/2P5/PP1PPPPP/RNBQKBNR w"
        game = init_game()

        user_move(game, MoveDto(fen="Pc2c3"))
        ai_move(game, MoveDto(fen="Nb8a6"))

        self.assertTrue(game.fen().startswith(fen))

    def test_user_illegal_move(self):
        game = init_game()
        with self.assertRaises(IllegalMoveError):
            user_move(game, MoveDto(fen="Pc2c5"))

    def test_ai_illegal_move(self):
        fen = "r1bqkbnr/pppppppp/8/8/2P5/8/PPnPPPPP/RNBQKBNR w"
        game = init_game()
        user_move(game, MoveDto(fen="Pc2c4"))
        ai_move(game, MoveDto(fen="Nb8c2"))
        self.assertTrue(game.fen().startswith(fen))
    
    def test_try_from_a_cell_do_not_have_any_piece(self):
        game = init_game()
        with self.assertRaises(AssertionError):
            ai_move(game, MoveDto(fen="Qa3a5"))

if __name__ == '__main__':
    unittest.main()
