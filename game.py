import requests
import json
import board

class Game:

    def __init__(self):
        self.gameboard = board.Board()

    def createFilePayload(self, values: dict, solution: dict) -> dict: # TODO: documentation
        payload = {
            "values": values,
            "solution": solution
        }
        return payload
    
    def dosukuInit(self): # TODO: documentation
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
                valuesToFile[self.gameboard.rows[r]+self.gameboard.cols[c]] = f'{grid[r][c]}'
                solutionToFile[self.gameboard.rows[r]+self.gameboard.cols[c]] = f'{solut[r][c]}'
        payloadForFile = self.createFilePayload(valuesToFile, solutionToFile) # TODO: use saveBoard to reduce repeat code.
        with open('scratch.json', 'w') as f:
            json.dump(payloadForFile, f, indent=4)

    def loadBoard(self): # TODO: documentation
        with open('scratch.json', 'r') as f:
            filecontents = json.loads(f.read())
            self.gameboard.sudokuBoard = filecontents['values']
            self.solution = filecontents['solution']

    def saveBoard(self): # TODO: documentation
        payload = self.createFilePayload(self.gameboard.sudokuBoard, self.gameboard.solution)
        with open('scratch.json', 'w') as f:
            json.dump(payload, f, indent=4)

    
    def checkBoard(self): # TODO: documentation
        if self.gameboard.solution == self.gameboard.sudokuBoard:
            return True
        return False