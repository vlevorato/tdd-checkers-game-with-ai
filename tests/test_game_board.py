import unittest
from game_board import GameBoard


class TestGameBoard(unittest.TestCase):
    def test_create_empty_board(self):
        board = GameBoard()
        self.assertEqual(len(board.squares), 8)
        for row in board.squares:
            self.assertEqual(len(row), 8)
            for square in row:
                self.assertIsNone(square)


if __name__ == '__main__':
    unittest.main()
