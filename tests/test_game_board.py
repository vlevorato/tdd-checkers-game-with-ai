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

    def test_initial_piece_placement(self):
        # Check white pieces
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 != 0:  # Black squares
                    piece = self.board.get_piece(i, j)
                    self.assertIsNotNone(piece)
                    self.assertEqual(piece.color, 'white')

        # Check black pieces
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 != 0:  # Black squares
                    piece = self.board.get_piece(i, j)
                    self.assertIsNotNone(piece)
                    self.assertEqual(piece.color, 'black')

        # Check middle rows are empty
        for i in range(3, 5):
            for j in range(8):
                piece = self.board.get_piece(i, j)
                self.assertIsNone(piece)

    def test_piece_count(self):
        white_count = sum(1 for row in self.board.squares for square in row
                          if square.piece and square.piece.color == 'white')
        black_count = sum(1 for row in self.board.squares for square in row
                          if square.piece and square.piece.color == 'black')
        self.assertEqual(white_count, 12)
        self.assertEqual(black_count, 12)

    def test_board_display(self):
        expected_display = (
            "  0 1 2 3 4 5 6 7\n"
            "0   O   O   O   O \n"
            "1 O   O   O   O   \n"
            "2   O   O   O   O \n"
            "3 .   .   .   .   \n"
            "4   .   .   .   . \n"
            "5 X   X   X   X   \n"
            "6   X   X   X   X \n"
            "7 X   X   X   X   \n"
        )
        self.assertEqual(self.board.display(), expected_display)


if __name__ == '__main__':
    unittest.main()
