class Board:

    sudokuBoard = {}
    rows = 'ABCDEFGHI'
    cols = '123456789'

    def __init__(self):
        self.sudokuBoard = {r+c:'0' for r in self.rows for c in self.cols}

    # textual grid output.
    def __str__(self):
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
