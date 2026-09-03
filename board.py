class Board:
    """A sudoku game board.

    Attributes:
        rows (str): Ordered and concatenated string of all the row names of the sudoku board.
        cols (str): Ordered and concatenated string of all the column names of the sudoku board.
        sudokuBoard (dict): Represents the state of the sudoku board where each entry is formatted coordinate (str): value (str).
            An empty square is stored as '0'.
        solution (dict): Holds the completed solution of the sudoku board in an identical format to sudokuBoard.

    """

    def __init__(self):
        """
        Parameters:

        """
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.sudokuBoard = {r+c:'0' for r in self.rows for c in self.cols}
        self.solution = {}

    def __str__(self): # TODO: documentation
        values = self.sudokuBoard.values()
        retStr = ''.join(values)
        return f'{retStr}'


    def displayboard(self): # TODO: documentation
        header = self.cols.partition('456')
        header = '|'.join(header)
        block = f'  {' '.join(header)}\n'
        for r in self.rows:
            if r == 'D' or r == 'G':
                block += '  - - - + - - - + - - -\n'
            for c in self.cols:
                if c == '4' or c == '7':
                    block += '| '
                elif c == '1':
                    block += f'{r} '
                block += self.sudokuBoard[r+c] if self.sudokuBoard[r+c] != '0' else ' '
                block += ' '
            block += '\n'
        print(block)

    def validateCoord(self, coord: str): # TODO: documentation
        if not ('A' <= coord[0] <= 'I' and '1' <= coord[1] <= '9'):
            raise ValueError('Invalid Square Coordinate')

    def validateValue(self, value: str): # TODO: documentation
        if not '1' <= value <= '9':
            raise ValueError('Invalid Game Value')

    def validateGameEntry(self, entryTup: tuple[str, str]): # TODO: documentation
        self.validateCoord(entryTup[0])
        self.validateValue(entryTup[1])

    def getsquare(self, sqCoord: str): # TODO: This function should not mess with the error. Call validate and return the value. No try except.
        try:
            self.validateCoord(sqCoord)
        except ValueError:
            pass
        else:
            return self.sudokuBoard[sqCoord]

    def fillsquare(self, sqCoord: str, value: str): # TODO: documentation
        try:
            self.validateGameEntry((sqCoord, value))
        except ValueError:
            pass
        else:
            self.sudokuBoard[sqCoord] = value


    def delsquare(self,sqCoord: str): # TODO: documentation
        try:
            self.validateCoord(sqCoord)
        except ValueError:
            pass
        else:
            self.sudokuBoard[sqCoord] = '0'
