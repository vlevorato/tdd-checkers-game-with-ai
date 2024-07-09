class Square:
    def __init__(self, color):
        self.color = color
        self.piece = None


class GameBoard:
    def __init__(self):
        self.squares = [[Square('white' if (i + j) % 2 == 0 else 'black')
                         for j in range(8)] for i in range(8)]

    def get_adjacent_squares(self, row, col):
        adjacent = []
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            new_row, new_col = row + i, col + j
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                adjacent.append(self.squares[new_row][new_col])
        return adjacent
