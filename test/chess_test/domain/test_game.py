import unittest
from datetime import datetime, timezone

from app.domain.game import Game
from app.dto.move_dto import UserMoveDto, PieceColor, PieceType, AIMoveDto, AIMoveType
from app.exception.game_exception import GameException
from app.schemas.chess_game_schema import ChessGameSchema


class GameTest(unittest.TestCase):
    sample_data = ChessGameSchema(
        game_status="ongoing",
        white="ai",
        moves=[],
        current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w",
        updated_at=datetime.now(timezone.utc)
    )

    def test_generate_game(self):
        game = Game(self.sample_data)

        # black is user
        self.assertEqual(game._user_role, False)
        # white is ai
        self.assertEqual(game._ai_role, True)
        # first turn is white
        self.assertEqual(game._turn, True)
        # not moved yet
        self.assertEqual(game.moves, [])

    def test_move(self):
        game = Game(self.sample_data)
        game.move(AIMoveDto(
            color=PieceColor.WHITE,
            piece=PieceType.PAWN,
            type=AIMoveType.MOV,
            start="a2",
            end="a4"
        ))

        self.assertEqual(game._turn, False)
        self.assertTrue(game.board.fen().startswith("rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR"))
        self.assertEqual(game.moves, ["a2a4"])

        game.move(UserMoveDto(
            color=PieceColor.BLACK,
            piece=PieceType.KNIGHT,
            start="b8",
            end="a6"
        ))

        self.assertEqual(game._turn, True)
        self.assertTrue(game.board.fen().startswith("r1bqkbnr/pppppppp/n7/8/P7/8/1PPPPPPP/RNBQKBNR"))
        self.assertEqual(game.moves, ["a2a4", "Nb8a6"])

    def test_illegal_move(self):
        game = Game(self.sample_data)
        # ai의 차례인대 유저가 움직이려 함
        with self.assertRaises(GameException):
            game.move(UserMoveDto(
                color=PieceColor.WHITE,
                piece=PieceType.KNIGHT,
                start="b1",
                end="a3"
            ))

        # ai가 유저의 기물(흑)을 움직이려 함
        with self.assertRaises(GameException):
            game.move(AIMoveDto(
                color=PieceColor.BLACK,
                piece=PieceType.KNIGHT,
                type=AIMoveType.MOV,
                start="b8",
                end="a6"
            ))

        # 유저의 차례인데 AI가 움직이려 함
        game = Game(self.sample_data.model_copy(update={ "white": "user" }))
        with self.assertRaises(GameException):
            game.move(AIMoveDto(
                color=PieceColor.WHITE,
                piece=PieceType.PAWN,
                type=AIMoveType.MOV,
                start="a2",
                end="a4"
            ))

        # 유저가 ai의 기물(흑)을 움직이려 함
        with self.assertRaises(GameException):
            game.move(AIMoveDto(
                color=PieceColor.BLACK,
                piece=PieceType.KNIGHT,
                type=AIMoveType.MOV,
                start="b8",
                end="a6"
            ))