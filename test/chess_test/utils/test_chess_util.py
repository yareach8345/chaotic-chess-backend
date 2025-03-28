import unittest

from chess import IllegalMoveError

from app.dto.move_dto import UserMoveDto, PieceColor, PieceType, AIMoveDto, AIMoveType
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

        user_move(game, UserMoveDto(
            color=PieceColor.WHITE,
            piece=PieceType.PAWN,
            start="c2",
            end="c3"))
        ai_move(game, AIMoveDto(
            type=AIMoveType.MOV,
            color=PieceColor.BLACK,
            piece=PieceType.KNIGHT,
            start="b8",
            end="a6"))

        self.assertTrue(game.fen().startswith(fen))

    def test_user_illegal_move(self):
        game = init_game()
        with self.assertRaises(IllegalMoveError):
            user_move(game, UserMoveDto(
                color=PieceColor.WHITE,
                piece=PieceType.PAWN,
                start="c2",
                end="c5"
            )),
    
    def test_ai_illegal_move(self):
        fen = "r1bqkbnr/pppppppp/8/8/2P5/8/PPnPPPPP/RNBQKBNR w"
        game = init_game()
        user_move(game, UserMoveDto(
            color=PieceColor.WHITE,
            piece=PieceType.PAWN,
            start="c2",
            end="c4"))
        ai_move(game, AIMoveDto(
            type=AIMoveType.MOV,
            color=PieceColor.BLACK,
            piece=PieceType.KNIGHT,
            start="b8",
            end="c2"
        ))
        self.assertTrue(game.fen().startswith(fen))
    
    def test_ai_generate_test(self):
        fen = "rnbqkbnr/pppppppp/8/Q7/8/8/PPPPPPPP/RNBQKBNR b"
        game = init_game()
        ai_move(game, AIMoveDto(
            type=AIMoveType.GEN,
            color=PieceColor.WHITE,
            piece=PieceType.QUEEN,
            end="a5"
        ))
        self.assertTrue(game.fen().startswith(fen))

if __name__ == '__main__':
    unittest.main()
