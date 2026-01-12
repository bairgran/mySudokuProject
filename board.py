class Board:
    """Abstract class Board provides some of the basic sudoku functionality.

    ...

    Attributes
    ----------
    sudokuBoard : dict
        Dictionary representing a 9x9 grid with axes [A-I] and [1-9].
    solution : dict
        Dictionary containing the solution of the sudoku board in the same format.
    rows : str
        Row names concatenated into a string.
    cols : str
        Column names concatenated into a string.

    Methods
    -------
    displayboard()
        Prints a textual representation of the current sudoku board.
    getsquare(sqCoord)
        returns the value associated with the square at coordinate sqCoord in the sudoku board.
    """

    def __init__(self):
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.sudokuBoard = {r+c:'0' for r in self.rows for c in self.cols}
        self.solution = {}

    # textual grid output.
    def __str__(self):
        return self.sudokuBoard.values()

    def displayboard(self):
        block = ''
        for r in self.rows:
            if r == 'D' or r == 'G':
                block += '- - - + - - - + - - -\n'
            for c in self.cols:
                if c == '4' or c == '7':
                    block += '| '
                block += self.sudokuBoard[r+c] if self.sudokuBoard[r+c] != '0' else ' '
                block += ' '
            block += '\n'
        print(block)

    def getsquare(self, sqCoord):
        if type(sqCoord) != str:
            print('Square must be a string')
            return -1
        if not ('A' <= sqCoord[0] <= 'I' or '1' <= sqCoord[1] <= '9'):
            print('Square must be a valid coordinate')
            return -1
        return self.sudokuBoard[sqCoord]