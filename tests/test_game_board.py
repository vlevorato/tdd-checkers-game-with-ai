import unittest
from game_board import GameBoard, Square, Piece


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
            "0   o   o   o   o \n"
            "1 o   o   o   o   \n"
            "2   o   o   o   o \n"
            "3 .   .   .   .   \n"
            "4   .   .   .   . \n"
            "5 x   x   x   x   \n"
            "6   x   x   x   x \n"
            "7 x   x   x   x   \n"
        )
        self.assertEqual(self.board.display(), expected_display)

    def test_valid_white_piece_move(self):
        self.assertTrue(self.board.move_piece([(2, 1), (3, 0)]))
        self.assertIsNone(self.board.get_piece(2, 1))
        self.assertIsNotNone(self.board.get_piece(3, 0))
        self.assertEqual(self.board.get_piece(3, 0).color, 'white')

    def test_valid_black_piece_move(self):
        self.assertTrue(self.board.move_piece([(5, 0), (4, 1)]))
        self.assertIsNone(self.board.get_piece(5, 0))
        self.assertIsNotNone(self.board.get_piece(4, 1))
        self.assertEqual(self.board.get_piece(4, 1).color, 'black')

    def test_invalid_moves(self):
        # Move to occupied square
        self.assertFalse(self.board.move_piece([(2, 1), (1, 0)]))

        # Move backwards
        self.assertFalse(self.board.move_piece([(2, 1), (1, 2)]))

        # Move horizontally
        self.assertFalse(self.board.move_piece([(2, 1), (2, 2)]))

        # Move more than one square
        self.assertFalse(self.board.move_piece([(2, 1), (4, 3)]))

        # Move from empty square
        self.assertFalse(self.board.move_piece([(3, 3), (4, 4)]))

    def test_valid_white_piece_capture(self):
        # Move a black piece to a position where it can be captured
        self.board.move_piece([(5, 0), (4, 1)])
        self.board.move_piece([(4, 1), (3, 2)])

        # Capture the black piece
        self.assertTrue(self.board.move_piece([(2, 1), (4, 3)]))
        self.assertIsNone(self.board.get_piece(2, 1))
        self.assertIsNone(self.board.get_piece(3, 2))
        self.assertIsNotNone(self.board.get_piece(4, 3))
        self.assertEqual(self.board.get_piece(4, 3).color, 'white')

    def test_valid_black_piece_capture(self):
        # Move a white piece to a position where it can be captured
        self.board.move_piece([(2, 1), (3, 2)])
        self.board.move_piece([(3, 2), (4, 3)])

        # Capture the white piece
        self.assertTrue(self.board.move_piece([(5, 2), (3, 4)]))
        self.assertIsNone(self.board.get_piece(5, 2))
        self.assertIsNone(self.board.get_piece(4, 3))
        self.assertIsNotNone(self.board.get_piece(3, 4))
        self.assertEqual(self.board.get_piece(3, 4).color, 'black')

    def test_invalid_captures(self):
        # Try to capture own piece
        self.board.move_piece([(2, 1), (3, 2)])
        self.assertFalse(self.board.move_piece([(2, 3), (4, 1)]))

        # Try to capture when there's no piece to capture
        self.assertFalse(self.board.move_piece([(2, 1), (4, 3)]))

        # Try to capture in wrong direction (backwards for white)
        self.board.move_piece([(5, 0), (4, 1)])
        self.assertFalse(self.board.move_piece([(2, 3), (0, 1)]))

    def test_multiple_capture_with_2_captures(self):
        # Set up a board state for multiple capture (2)
        self.board = GameBoard()
        self.board.squares[3][2].piece = Piece('black')
        self.board.squares[5][4].piece = Piece('black')
        self.board.squares[6][5].piece = None

        # Perform a multiple capture
        moves = [(2, 1), (4, 3), (6, 5)]
        self.assertTrue(self.board.move_piece(moves))

        # Check that the piece has moved to the final position
        self.assertIsNone(self.board.get_piece(2, 1))
        self.assertIsNotNone(self.board.get_piece(6, 5))
        self.assertEqual(self.board.get_piece(6, 5).color, 'white')

        # Check that the captured pieces are removed
        self.assertIsNone(self.board.get_piece(3, 2))
        self.assertIsNone(self.board.get_piece(5, 4))

    def test_invalid_multiple_capture_with_2_captures(self):
        # Set up a board state for multiple capture (2)
        self.board = GameBoard()
        self.board.squares[3][2].piece = Piece('black')
        self.board.squares[3][4].piece = Piece('black')
        self.board.squares[5][4].piece = None
        self.board.squares[5][6].piece = None

        # Try to perform an invalid multiple capture (no piece to capture in the second jump)
        moves = [(2, 1), (4, 3), (2, 5)]
        self.assertFalse(self.board.move_piece(moves))

        # Check that no pieces have moved or been captured
        self.assertIsNotNone(self.board.get_piece(2, 1))
        self.assertIsNotNone(self.board.get_piece(2, 5))
        self.assertIsNotNone(self.board.get_piece(3, 2))
        self.assertIsNone(self.board.get_piece(4, 3))

    def test_multiple_capture_change_direction_with_2_captures(self):
        # Set up a board state for multiple capture (2) with direction change
        self.board = GameBoard()
        self.board.squares[3][2].piece = Piece('black')
        self.board.squares[6][1].piece = None

        # Perform a multiple capture with direction change
        moves = [(2, 1), (4, 3), (6, 1)]
        self.assertTrue(self.board.move_piece(moves))

        # Check that the piece has moved to the final position
        self.assertIsNone(self.board.get_piece(2, 1))
        self.assertIsNone(self.board.get_piece(4, 3))
        self.assertIsNotNone(self.board.get_piece(6, 1))
        self.assertEqual(self.board.get_piece(6, 1).color, 'white')

        # Check that the captured pieces are removed
        self.assertIsNone(self.board.get_piece(3, 2))
        self.assertIsNone(self.board.get_piece(5, 2))

    def test_multiple_capture_with_3_captures(self):
        # Set up a board state for multiple capture (3)
        self.board = GameBoard()
        self.board.squares[2][1].piece = Piece('black')
        self.board.squares[4][3].piece = Piece('black')
        self.board.squares[5][4].piece = None
        self.board.squares[7][6].piece = None

        # Perform a multiple capture
        moves = [(1, 0), (3, 2), (5, 4), (7, 6)]
        self.assertTrue(self.board.move_piece(moves))

        # Check that the piece has moved to the final position
        self.assertIsNone(self.board.get_piece(1, 0))
        self.assertIsNone(self.board.get_piece(3, 2))
        self.assertIsNone(self.board.get_piece(5, 4))
        self.assertIsNotNone(self.board.get_piece(7, 6))
        self.assertEqual(self.board.get_piece(7, 6).color, 'white')

        # Check that the captured pieces are removed
        self.assertIsNone(self.board.get_piece(2, 1))
        self.assertIsNone(self.board.get_piece(4, 3))
        self.assertIsNone(self.board.get_piece(6, 5))

    def test_invalid_multiple_capture_with_3_captures(self):
        # Set up a board state for multiple capture (3)
        self.board = GameBoard()
        self.board.squares[2][1].piece = Piece('black')
        self.board.squares[4][3].piece = Piece('black')
        self.board.squares[5][4].piece = None

        # Try to perform an invalid multiple capture (no piece to capture in the third jump)
        moves = [(1, 0), (3, 2), (5, 4), (7, 6)]
        self.assertFalse(self.board.move_piece(moves))

        # Check that no pieces have moved or been captured
        self.assertIsNotNone(self.board.get_piece(1, 0))
        self.assertIsNotNone(self.board.get_piece(2, 1))
        self.assertIsNone(self.board.get_piece(3, 2))
        self.assertIsNotNone(self.board.get_piece(4, 3))
        self.assertIsNone(self.board.get_piece(5, 4))
        self.assertIsNotNone(self.board.get_piece(6, 5))
        self.assertIsNotNone(self.board.get_piece(7, 6))

    def test_white_piece_becomes_king(self):
        # Setup: Move a white piece to the last row
        self.board = GameBoard()
        self.board.squares[7][0].piece = None
        self.board.squares[6][1].piece = Piece('white')

        # Action: Move the white piece to the last row
        self.assertTrue(self.board.move_piece([(6, 1), (7, 0)]))

        # Assert: The piece should now be a king
        piece = self.board.get_piece(7, 0)
        self.assertIsNotNone(piece)
        self.assertEqual(piece.color, 'white')
        self.assertTrue(piece.is_king)

    def test_black_piece_becomes_king(self):
        # Setup: Move a black piece to the last row
        self.board = GameBoard()
        self.board.squares[0][1].piece = None
        self.board.squares[1][0].piece = Piece('black')

        # Action: Move the black piece to the last row
        self.assertTrue(self.board.move_piece([(1, 0), (0, 1)]))

        # Assert: The piece should now be a king
        piece = self.board.get_piece(0, 1)
        self.assertIsNotNone(piece)
        self.assertEqual(piece.color, 'black')
        self.assertTrue(piece.is_king)

    def test_piece_does_not_become_king_on_other_rows(self):
        # Setup: Move a piece to a non-last row
        self.board = GameBoard()
        self.board.squares[2][1].piece = None
        self.board.squares[3][2].piece = Piece('white')

        # Action: Move the piece
        self.assertTrue(self.board.move_piece([(3, 2), (4, 3)]))

        # Assert: The piece should not be a king
        piece = self.board.get_piece(4, 3)
        self.assertIsNotNone(piece)
        self.assertEqual(piece.color, 'white')
        self.assertFalse(piece.is_king)

    def test_king_move_backwards(self):
        self.board = GameBoard()
        self.board.squares[5][2].piece = Piece('white')
        self.board.squares[5][2].piece.is_king = True

        # Move backwards
        self.assertTrue(self.board.move_piece([(5, 2), (4, 1)]))
        self.assertIsNone(self.board.get_piece(5, 2))
        self.assertIsNotNone(self.board.get_piece(4, 1))
        self.assertEqual(self.board.get_piece(4, 1).color, 'white')
        self.assertTrue(self.board.get_piece(4, 1).is_king)

    def test_king_capture_backwards(self):
        self.board = GameBoard()
        self.board.squares[5][2].piece = Piece('white')
        self.board.squares[5][2].piece.is_king = True
        self.board.squares[4][3].piece = Piece('black')

        # Capture backwards
        self.assertTrue(self.board.move_piece([(5, 2), (3, 4)]))
        self.assertIsNone(self.board.get_piece(5, 2))
        self.assertIsNone(self.board.get_piece(4, 3))
        self.assertIsNotNone(self.board.get_piece(3, 4))
        self.assertEqual(self.board.get_piece(3, 4).color, 'white')
        self.assertTrue(self.board.get_piece(3, 4).is_king)

    def test_king_multiple_capture(self):
        self.board = GameBoard()
        self.board.squares[5][2].piece = Piece('white')
        self.board.squares[5][2].piece.is_king = True
        self.board.squares[2][3].piece = Piece('black')
        self.board.squares[4][3].piece = Piece('black')
        self.board.squares[1][2].piece = None

        # Multiple capture, changing direction
        self.assertTrue(self.board.move_piece([(5, 2), (3, 4), (1, 2)]))
        self.assertIsNone(self.board.get_piece(5, 2))
        self.assertIsNone(self.board.get_piece(4, 3))
        self.assertIsNone(self.board.get_piece(2, 3))
        self.assertIsNotNone(self.board.get_piece(1, 2))
        self.assertEqual(self.board.get_piece(1, 2).color, 'white')
        self.assertTrue(self.board.get_piece(1, 2).is_king)

    def test_king_invalid_long_move(self):
        self.board = GameBoard()
        self.board.squares[5][2].piece = Piece('white')
        self.board.squares[5][2].piece.is_king = True

        # Try to move more than one square
        self.assertFalse(self.board.move_piece([(5, 2), (3, 4)]))
        self.assertIsNotNone(self.board.get_piece(5, 2))
        self.assertIsNone(self.board.get_piece(3, 4))


if __name__ == '__main__':
    unittest.main()
