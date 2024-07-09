import unittest
from game_board import GameBoard, Square


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.board = GameBoard()

    def test_create_empty_board(self):
        self.assertEqual(len(self.board.squares), 8)
        for row in self.board.squares:
            self.assertEqual(len(row), 8)
            for square in row:
                self.assertIsInstance(square, Square)

    def test_alternating_colors(self):
        for i in range(8):
            for j in range(8):
                expected_color = 'white' if (i + j) % 2 == 0 else 'black'
                self.assertEqual(self.board.squares[i][j].color, expected_color)

    def test_bottom_right_square_white(self):
        self.assertEqual(self.board.squares[7][7].color, 'white')

    def test_adjacent_squares_different_colors(self):
        for i in range(8):
            for j in range(8):
                current_color = self.board.squares[i][j].color
                adjacent_squares = self.board.get_adjacent_squares(i, j)
                for adj_square in adjacent_squares:
                    self.assertNotEqual(current_color, adj_square.color)

    def test_get_adjacent_squares(self):
        # Test for a corner square (should have 2 adjacent squares)
        adjacent = self.board.get_adjacent_squares(0, 0)
        self.assertEqual(len(adjacent), 2)

        # Test for an edge square (should have 3 adjacent squares)
        adjacent = self.board.get_adjacent_squares(0, 1)
        self.assertEqual(len(adjacent), 3)

        # Test for a middle square (should have 4 adjacent squares)
        adjacent = self.board.get_adjacent_squares(3, 3)
        self.assertEqual(len(adjacent), 4)


if __name__ == '__main__':
    unittest.main()
