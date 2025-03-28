import unittest

from app.dto.move_dto import UserMoveDto, PieceType, PieceColor, AIMoveDto, AIMoveType


class MoveDtoTest(unittest.TestCase):
    def test_to_uci(self):
        move_dto = UserMoveDto(
            color=PieceColor.WHITE,
            piece=PieceType.PAWN,
            start="a4",
            end="b5"
        )

        self.assertEqual(move_dto.to_uci(), "a4b5")

    def test_to_piece(self):
        move_dto1 = UserMoveDto(
            color=PieceColor.WHITE,
            piece=PieceType.PAWN,
            start="a4",
            end="b5"
        )

        piece1 = move_dto1.to_piece()
        self.assertEqual(piece1.symbol(), "P")

        move_dto2 = UserMoveDto(
            color=PieceColor.BLACK,
            piece=PieceType.QUEEN,
            start="a4",
            end="b5"
        )

        piece2 = move_dto2.to_piece()
        self.assertEqual(piece2.symbol(), "q")

    def test_to_algebraic(self):
        move_dto1 = UserMoveDto(
            color=PieceColor.WHITE,
            piece=PieceType.PAWN,
            start="a4",
            end="b5"
        )

        algebraic1 = move_dto1.to_algebraic()
        self.assertEqual(algebraic1, "a4b5")

        move_dto2 = UserMoveDto(
            color=PieceColor.WHITE,
            piece=PieceType.BISHOP,
            start="a4",
            end="c6"
        )

        algebraic2 = move_dto2.to_algebraic()
        self.assertEqual(algebraic2, "Ba4c6")

        move_dto3 = UserMoveDto(
            color=PieceColor.BLACK,
            piece=PieceType.QUEEN,
            start="a4",
            end="b5"
        )

        algebraic3 = move_dto3.to_algebraic()
        self.assertEqual(algebraic3, "Qa4b5")

        move_dto4 = AIMoveDto(
            color=PieceColor.WHITE,
            type=AIMoveType.GEN,
            piece=PieceType.QUEEN,
            start="a1",
            end="c7"
        )

        algebraic4 = move_dto4.to_algebraic()
        self.assertEqual(algebraic4, "Q??c7")


if __name__ == '__main__':
    unittest.main()
