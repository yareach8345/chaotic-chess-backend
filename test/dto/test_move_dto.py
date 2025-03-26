import unittest

from app.dto.move_dto import UserMoveDto, PieceType, PieceColor


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


if __name__ == '__main__':
    unittest.main()
