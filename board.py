class Board:

    sudokuBoard = {}
    rows = 'ABCDEFGHI'
    cols = '123456789'

    def __init__(self):
        self.sudokuBoard = {r+c:'0' for r in self.rows for c in self.cols}

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
        return block

    def getsquare(self, sqCoord):
        if type(sqCoord) != str:
            print('Square must be a string')
            return -1
        if not ('A' <= sqCoord[0] <= 'I' or '1' <= sqCoord[1] <= '9'):
            print('Square must be a valid coordinate')
            return -1
        return self.sudokuBoard[sqCoord]