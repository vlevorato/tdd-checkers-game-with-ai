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
