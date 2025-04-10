import unittest

import chess

from app.dto.move_dto import MoveDto

class MoveDtoTest(unittest.TestCase):
    move_dto = MoveDto(moving="Qa1d1")

    def test_to_uci(self):
        self.assertEqual(self.move_dto.to_uci(), "a1d1")

    def test_get_piece(self):
        self.assertEqual(self.move_dto.get_piece().piece_type, 5)

    def test_get_start_square(self):
        self.assertEqual(self.move_dto.get_start_square(), chess.parse_square("a1"))

    def test_get_end_square(self):
        self.assertEqual(self.move_dto.get_end_square(), chess.parse_square("d1"))

if __name__ == '__main__':
    unittest.main()
