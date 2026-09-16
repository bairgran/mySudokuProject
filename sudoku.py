"""Module for playing a game of sudoku.

This module contains all the logic and state information for a sudoku game. 
Sudoku handles the game loop and all player level functionality.
Board contains the state of the game board.

This module is meant to function as a CLI app.

Typical usage:

    foo = Sudoku()
    foo.start()
"""
import requests
import json

class Sudoku:
    """Sudoku game.

    Call start() on an instance of Sudoku to begin playing.

    Attributes:
        board: The Board currently being used in the game.
    """
    def __init__(self):
        """Initializes a Board object to be used with this instance."""
        self.board = Board()

    # start() is the "main menu" entry point. Enters loop where possible actions are new, load, exit, and start(if board). 
    # create_game() creates a new board currently through dosuku API. Board is output to scratch.json and held in self.board.
    # load_game() loads the board state (if any) from scratch.json into self.board.
    # If self.board is loaded, option to start is selected
    # run() enters the game loop if a board is loaded.
    # exit() returns


    def start(self):
        pass


    def load_game(self):
        pass

    def save_game(self):
        pass

    def run(self):
        pass

    def exit(self):
        pass
    # Expected functionality:
    # - Create a new game
    # - Load a game from a file
    # - Save a game to a file
    # - Enter game loop


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
        self.sudoku_board = {r+c:'0' for r in self.rows for c in self.cols}
        self.solution = self.sudoku_board.copy()


    def set_board(self, values: list[list]) -> None:
        for key in self.sudoku_board:
            self.sudoku_board[key] = f'{values[self.rows.index(key[0])][int(key[1])-1]}'

    def set_solution(self, values: list[list]) -> None:
        for key in self.solution:
            self.solution[key] = f'{values[self.rows.index(key[0])][int(key[1])-1]}'

    def get_state(self) -> dict:
        return {"values": self.sudoku_board, "solution": self.solution}

    def write_tile(self, coord: str, value: str):
        pass

    def del_tile(self, coord: str):
        pass

    def is_solved(self) -> bool:
        return self.sudoku_board == self.solution
    

def _create_game_data(init_type: str = "dosuku") -> Board: # TODO: Alternate data creation methods.
    """Create game save data.

    Creates game save data by the desired method. Defaults to pulling data from Dosuku API.

    Args:
        init_type: A string representing the desired creation method.
    """
    ret_board = Board.board()
    if init_type == "dosuku":
        url_api = "https://sudoku-api.vercel.app/api/dosuku"
        query = {'query': '{newboard(limit:1){grids{value,solution}}}'}
        r = requests.get(url_api, params=query)
        data = r.json()
        grid = data['newboard']['grids'][0]['value']
        solut = data['newboard']['grids'][0]['solution']
        ret_board.set_board(grid)
        ret_board.set_solution(solut)
    return ret_board