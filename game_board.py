class Square:
    def __init__(self, color):
        self.color = color
        self.piece = None


class Piece:
    def __init__(self, color):
        self.color = color


class GameBoard:
    def __init__(self):
        self.squares = [[Square('white' if (i + j) % 2 == 0 else 'black')
                         for j in range(8)] for i in range(8)]
        self._setup_initial_pieces()

    def get_adjacent_squares(self, row, col):
        adjacent = []
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            new_row, new_col = row + i, col + j
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                adjacent.append(self.squares[new_row][new_col])
        return adjacent

    def _setup_initial_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.squares[i][j].color == 'black':
                    if i < 3:
                        self.squares[i][j].piece = Piece('white')
                    elif i > 4:
                        self.squares[i][j].piece = Piece('black')

    def get_piece(self, row, col):
        return self.squares[row][col].piece

    def display(self):
        board_str = "  0 1 2 3 4 5 6 7\n"
        for i, row in enumerate(self.squares):
            board_str += f"{i} "
            for square in row:
                if square.piece is None:
                    board_str += '.' if square.color == 'black' else ' '
                else:
                    board_str += 'O' if square.piece.color == 'white' else 'X'
                board_str += ' '
            board_str += '\n'
        return board_str

    def _get_move_type(self, from_row, from_col, to_row, to_col):
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8):
            return None

        piece = self.squares[from_row][from_col].piece
        if piece is None or self.squares[to_row][to_col].piece is not None:
            return None

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        if piece.color == 'white':
            if row_diff == 1 and abs(col_diff) == 1:
                return 'move'
            elif row_diff == 2 and abs(col_diff) == 2:
                mid_row, mid_col = (from_row + to_row) // 2, (from_col + to_col) // 2
                if self.squares[mid_row][mid_col].piece and self.squares[mid_row][mid_col].piece.color == 'black':
                    return 'capture'
        else:  # black piece
            if row_diff == -1 and abs(col_diff) == 1:
                return 'move'
            elif row_diff == -2 and abs(col_diff) == 2:
                mid_row, mid_col = (from_row + to_row) // 2, (from_col + to_col) // 2
                if self.squares[mid_row][mid_col].piece and self.squares[mid_row][mid_col].piece.color == 'white':
                    return 'capture'

        return None

    def move_piece(self, from_row, from_col, to_row, to_col):
        move_type = self._get_move_type(from_row, from_col, to_row, to_col)
        if move_type is None:
            return False

        piece = self.squares[from_row][from_col].piece
        self.squares[to_row][to_col].piece = piece
        self.squares[from_row][from_col].piece = None

        if move_type == 'capture':
            mid_row, mid_col = (from_row + to_row) // 2, (from_col + to_col) // 2
            self.squares[mid_row][mid_col].piece = None

        return True

    def _is_valid_move(self, from_row, from_col, to_row, to_col):
        # Check if the move is within the board
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8):
            return False

        # Check if there's a piece at the starting position
        piece = self.squares[from_row][from_col].piece
        if piece is None:
            return False

        # Check if the destination is empty
        if self.squares[to_row][to_col].piece is not None:
            return False

        # Check if the move is diagonal and forward
        if piece.color == 'white':
            return to_row == from_row + 1 and abs(to_col - from_col) == 1
        else:  # black piece
            return to_row == from_row - 1 and abs(to_col - from_col) == 1
