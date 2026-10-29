"""Module for playing a game of sudoku.

This module contains all the logic and state information for a sudoku game. 
Sudoku handles the game loop and all player level functionality.
Board contains the state of the game board. Board tiles are addressed
by coordinates made of a row letter ('A' through 'I') followed by a column
digit ('1' through '9'), for example 'A1' or 'E5'. Tile values are digit
strings, and '0' marks an empty tile.

Typical usage:

"""
import requests
import json


SAVE_FILE = 'scratch.json'


class Sudoku:
    """Sudoku game session.

    Can start new games and load saved games.

    Attributes:
        board: The Board currently being used in the game.
    """
    def __init__(self):
        """Initializes a Board object to be used with this instance."""
        self.board = Board()

    # start() is the "main menu" entry point. Enters loop where possible
    #   actions are new, load, exit, and start(if board).
    # create_game() creates a new board currently through dosuku API.
    #   Board is output to scratch.json and held in self.board.
    # load_game() loads the board state (if any) from scratch.json into
    #   self.board.
    # If self.board is loaded, option to start is selected
    # run() enters the game loop if a board is loaded.
    # exit() returns


    def start(self):
        pass

    def new_game(self):
        """Create new puzzle.
        
        Generates new game data, writes data to SAVE_FILE,
        and loads newly created game data.
        Overwrites any data contained in SAVE_FILE.
        """
        _write_to_save(_create_game_data())
        self.load_game()

    def load_game(self):
        """Load existing game data.
        
        Loads the puzzle and solution data from SAVE_FILE into self.board.
        """
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            self.board.sudoku_board = data['values']
            self.board.solution = data['solution']

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
    """A 9x9 sudoku game board holding current tile and solution values.

    Attributes:
        sudoku_board: A dict mapping the coordinate string
            (coord[0] = 'A'-'I', coord[1] = '1'-'9') of every tile to the
            current value of that tile (value = '1'-'9')
            as a digit string (e.g., 'A1': '5').
            Empty tiles are marked with '0'.
        solution: A dict mapping each tile coordinate to its solution value.
            Formatted identical to sudoku_board.
    """

    _ROWS = 'ABCDEFGHI'
    _COLS = '123456789'
    _EMPTY_TILE = '0'
    _TILE_VALUES = '123456789'

    def __init__(self):
        """Initialize the board with every tile and solution value empty."""
        self._sudoku_board = {
            r+c:Board._EMPTY_TILE for r in Board._ROWS for c in Board._COLS}
        self._solution = self._sudoku_board.copy()

    def set_state(self, board: list[list[int]], sol: list[list[int]]) -> bool:
        """Set the current board state.

        Args:
            board: A 9x9 2D array of ints 0-9. Empty tiles must be represented
                as 0.
            sol: A 9x9 2D array of ints 1-9.

        Returns:
            True on successful set, False on failure.
        """
        temp_board = {}
        temp_solution = {}
        for key in self._sudoku_board:
            row = Board._ROWS.index(key[0])
            col = int(key[1]-1)
            value = str(board[row][col])
            solution_value = str(sol[row][col])
            if (
                not self._validate_value(value, accept_empty=True)
                or not self._validate_value(solution_value, accept_empty=False)
            ):
                return False
            temp_board[key] = value
            temp_solution[key] = solution_value
        self._sudoku_board = temp_board
        self._solution = temp_solution
        return True

    def set_board(self, values: list[list]) -> None:
        """Set the current tile values.
        
        Args:
            values: A 9x9 2D array of ints 0-9. Empty tiles must be represented
                as 0.
        """
        for key in self._sudoku_board:
            row = Board._ROWS.index(key[0])
            col = int(key[1])-1
            self._sudoku_board[key] = f'{values[row][col]}'

    def set_solution(self, values: list[list]) -> None:
        """Set the solution values.

        Args:
            values: A 9x9 2D array of ints 1-9.
        """
        for key in self._solution:
            row = Board._ROWS.index(key[0])
            col = int(key[1])-1
            self._solution[key] = f'{values[row][col]}'

    def get_state(self) -> dict:
        """Return the current tile values and solution.
        
        Returned dict has two keys, 'values' and 'solution', mapping directly 
        to self._sudoku_board and self._solution respectively. Returned dicts
        are the boards own objects, not copies.
        """
        return {'values': self._sudoku_board, 'solution': self._solution}

    def write_tile(self, coord: str, value: str) -> bool:
        """Write a value to a tile.

        Args:
            coord: The coordinate of the tile (e.g., 'A1').
            value: The digit string to be written, '0'-'9'.
        
        Returns:
            True on successful write, False on failure.
        """
        if (
            not self._validate_coordinate(coord)
            or not self._validate_value(value)
        ):
            return False
        self._sudoku_board[coord] = value
        return True

    def del_tile(self, coord: str) -> None:
        """Clear a tile.
        
        Sets value of tile to '0'. 

        Args:
            coord: The coordinate of the tile (e.g., 'A1').
        """
        self._sudoku_board[coord] = Board._EMPTY_TILE

    def is_solved(self) -> bool:
        """Returns True if every tile matches the solution, else False."""
        return self._sudoku_board == self._solution

    def _validate_coordinate(self, coordinate: str) -> bool:
        """Check for valid coordinate.
        
        A valid coordinate is a 2 character string where str[0] in Board._ROWS
        and str[1] in Board._COLS.

        Args:
            coordinate: The coordinate string to be validated.

        Returns:
            True if coordinate meets requirements, False if not.
        """
        if (
            len(coordinate) == 2
            and coordinate[0] in Board._ROWS
            and coordinate[1] in Board._COLS
        ):
            return True
        return False

    def _validate_value(self, value: str, accept_empty: bool=True) -> bool:
        """Check for valid value.
        
        A valid value is a single digit string from '1'-'9'.
        '0' is valid if accept_empty flag is True.
        
        Args:
            value: Single digit string to be validated.
            accept_empty: optional bool for if '0' is valid or not.

        Returns:
            True if value is valid, False if not.
        """
        if (
            len(value) == 1
            and (value in Board._TILE_VALUES
                 or (accept_empty and value in Board._EMPTY_TILE))
        ):
            return True
        return False


def _create_game_data(init_type: str = 'dosuku') -> Board:
    # TODO: Alternate data creation methods.
    """Create game save data.

    Creates a board populated with new data. Data generation methods
    are currently limited to dosuku API.

    Args:
        init_type: Represents the desired creation method.

    Returns:
        A Board whose values and solution are newly generated.
    """
    ret_board = Board()
    if init_type == 'dosuku':
        url_api = 'https://sudoku-api.vercel.app/api/dosuku'
        query = {'query': '{newboard(limit:1){grids{value,solution}}}'}
        r = requests.get(url_api, params=query, timeout=5)
        data = r.json()
        grid = data['newboard']['grids'][0]['value']
        solut = data['newboard']['grids'][0]['solution']
        ret_board.set_board(grid)
        ret_board.set_solution(solut)
    return ret_board


def _write_to_save(board_state: Board) -> None:
    """Write board_state to output file.

    Args:
        board_state: Board whos state is written to SAVE_FILE.
    """
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(board_state.get_state(), f, indent=4)


class CoordinateError(ValueError):
    """Coordinate input is invalid."""


class TileError(ValueError):
    """Tile input value is invalid."""


class BoardFormatError(Exception):
    """Container does not represent a properly formatted board."""
