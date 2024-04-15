import numpy as np
import itertools as it
from enum import Enum
from typing import TYPE_CHECKING
from sys import path
from os import path as ospath

# Weird way to import the classes from the parent directory
current_dir = ospath.dirname(ospath.relpath(__file__))
parent_dir = ospath.dirname(current_dir)
parent_dir = ospath.dirname(parent_dir)
path.append(parent_dir)

from gamescollection.custom_io.classes import CL_Interface, IO_Interface

if TYPE_CHECKING:
    pass


class Player(Enum):
    """Enum for the two players in the game"""

    WHITE = 0
    BLACK = 1
    EMPTY = 2

    def __str__(self) -> str:
        if self == Player.WHITE:
            return "X"
        elif self == Player.BLACK:
            return "O"
        else:
            return "."


class Tile:
    """Class which represents a single tile on the board"""

    def __init__(self) -> None:
        """Default constructor"""
        self.x = -1
        self.y = -1
        self.player = Player.EMPTY

    def __init__(self, x: int, y: int, player: Player) -> None:
        self.x = x
        self.y = y
        self.player = player

    def __str__(self) -> str:
        return str(self.player)


class Hex:
    """Class which represents the game of Hex.

    Attributes:

    """

    def __init__(
        self,
        size: int,
        in_interface: IO_Interface,
        out_interface: IO_Interface,
    ) -> None:
        self._board = np.ndarray((size, size), dtype=Tile)
        self._graph = np.ndarray((size * size, 0), dtype=Tile)
        self._size = size
        self._in_interface = in_interface
        self._out_interface = out_interface

        north = Tile(-1, -1, Player.WHITE)
        south = Tile(-1, -1, Player.WHITE)
        east = Tile(-1, -1, Player.BLACK)
        west = Tile(-1, -1, Player.BLACK)

        for x, y in it.product(range(self._size), repeat=2):
            self._board[x, y] = Tile(x, y, Player.EMPTY)

    def print_board(self) -> None:
        """Print the current state of the board"""
        out_str: str = ""
        indent: str = ""
        for x in range(self._size):
            out_str += indent

            out_str += " - ".join(
                [str(self._board[x, y].player) for y in range(self._size)]
            )
            out_str += "\n"
            if x < self._size - 1:
                out_str += indent + " "
                out_str += "\\ / ".join("" for _ in range(self._size))
                out_str += "\\" + "\n"

            indent += "  "

        self._out_interface.out(out_str)

    def make_move(self, x: int, y: int, player: Player) -> bool:
        """Method to make a move on the board.

        Method evaluates if the move is legal and returns True if the move was made successfully.

        Args:
            x (int): X coordinate of the Tile on the board.
            y (int): Y coordinate of the Tile on the board.
            player (Player): Player who makes the move

        Returns:
            bool: _description_
        """
        if x < 0 or x >= self._size or y < 0 or y >= self._size:
            return False
        elif self._board[x, y].player != Player.EMPTY and player != Player.EMPTY:
            self._board[x, y].player = player
            return True
        else:
            return False

    def _update_board(self, x: int, y: int, player: Player) -> None:
        pass

    def _undo_move(self, x: int, y: int) -> None:
        """Method to undo a move on the board.

        Needed for fast and efficient simulation of Games

        Args:
            x (int): X coordinate of the Tile on the board.
            y (int): Y coordinate of the Tile on the board.
        """
        self._board[x, y].player = Player.EMPTY


cli = CL_Interface()
hex = Hex(11, cli, cli)
hex.print_board()
