import numpy as np
import itertools as it
from enum import Enum
from typing import TYPE_CHECKING

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


def tile_constructor(x: int, y: int, player: Player):
    """Function to construct tile for the board

    Function is used instead of a class to save memory and compute time.

    Args:
        x (int): x-coordinate of the tile
        y (int): y-coordinate of the tile
        player (Player): Player who owns the tile

    Returns:
        dict: Dictionary representing the tile
    """
    return {"x": x, "y": y, "player": player}


class Hex:
    """Class which represents the game of Hex.

    Attributes:

    """

    def __init__(
        self,
        size: int,
        in_interface,
        out_interface,
    ) -> None:
        self._board = np.ndarray((size, size), dtype=dict)
        self._size = size
        self._in_interface = in_interface
        self._out_interface = out_interface

        for x, y in it.product(range(self._size), repeat=2):
            self._board[x, y] = tile_constructor(x, y, Player.EMPTY)

    def print_board(self):
        """Print the current state of the board"""
        for x in range(self._size):
            print(" " * x, end="")
            print(
                " - ".join(
                    [str(self._board[x, y]["player"]) for y in range(self._size)]
                )
            )


hex = Hex(5, None, None)
hex.print_board()
