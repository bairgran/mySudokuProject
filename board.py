import requests
import json

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
        """
        Paramters
        ---------
        """
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.sudokuBoard = {r+c:'0' for r in self.rows for c in self.cols}
        self.solution = {}

    def __str__(self):
        iter = self.sudokuBoard.values()
        retStr = ''
        for x in iter:
            retStr += x
        return retStr

    def dusokuInit(self):
        url_api = "https://sudoku-api.vercel.app/api/dosuku"
        query = {'query': '{newboard(limit:1){grids{value,solution}}}'}
        r = requests.get(url_api, params=query)
        data = r.json()
        grid = data['newboard']['grids'][0]['value']
        solut = data['newboard']['grids'][0]['solution']
        valuesToFile = {}
        solutionToFile = {}
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                valuesToFile[self.rows[r]+self.cols[c]] = f'{grid[r][c]}'
                solutionToFile[self.rows[r]+self.cols[c]] = f'{solut[r][c]}'
        payloadForFile = {
            "values": valuesToFile,
            "solution": solutionToFile
        }
        with open('scratch.json', 'w') as f:
            json.dump(payloadForFile, f, indent=4)

    def loadBoard(self):
        with open('scratch.json', 'r') as f:
            filecontents = json.loads(f.read())
            self.sudokuBoard = filecontents['values']
            self.solution = filecontents['solution']

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

    def validateCoord(self, coord: str):
        if not ('A' <= coord[0] <= 'I' and '1' <= coord[1] <= '9'):
            raise ValueError('Square must be a valid coordinate')

    def validateValue(self, value: str):
        if not '1' <= value <= '9':
            raise ValueError('Entry must be a valid value')

    def validateGameEntry(self, entryTup: tuple[str, str]):
        self.validateCoord(entryTup[0])
        self.validateValue(entryTup[1])

    def getsquare(self, sqCoord: str):
        try:
            self.validateCoord(sqCoord)
        except ValueError:
            pass
        else:
            return self.sudokuBoard[sqCoord]

    def fillsquare(self, sqCoord: str, value: str):
        try:
            self.validateGameEntry((sqCoord, value))
        except ValueError:
            pass
        else:
            self.sudokuBoard[sqCoord] = value


    def delsquare(self,sqCoord: str):
        try:
            self.validateCoord(sqCoord)
        except ValueError:
            pass
        else:
            self.sudokuBoard[sqCoord] = '0'