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

    def __repr__(self) -> str:
        return f"({self.x}, {self.y} | {self.player})"

    def __eq__(self, value: object) -> TYPE_CHECKING:
        return self.x == value.x and self.y == value.y and self.player == value.player

    def __ne__(self, value: object) -> TYPE_CHECKING:
        return not self.__eq__(value)

    def __hash__(self) -> int:
        return hash(f"{self.x}, {self.y}")


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
        self._size = size
        self._in_interface = in_interface
        self._out_interface = out_interface
        self._round = 0

        # Special Tiles for the edges of the board
        self._north = Tile(-1, -2, Player.WHITE)
        self._south = Tile(-2, -2, Player.WHITE)
        self._east = Tile(-2, -3, Player.BLACK)
        self._west = Tile(-3, -3, Player.BLACK)

        # Virtual Tile, needed to make array homogenous
        self._virtual_tile = Tile(-1, -1, Player.EMPTY)
        self._board = np.ndarray((size, size), dtype=Tile)

        # Initialize the board with empty Tiles
        for x, y in it.product(range(self._size), repeat=2):
            self._board[x, y] = Tile(x, y, Player.EMPTY)

        # Create the Graph which represents the board
        self._graph = self._create_graph(size)
        assert id(self._graph[0, 0]) == id(self._board[0, 1])

    def _create_graph(self, size: int) -> np.ndarray:
        """Create the Graph tha represents the Hex game based on size
        First create list of lists and then convert to numpy array is faster than creating ndarray directly and populating it

        Since Arrays need to be homogenous to perform best, some Tiles have connections to "virtual" nodes which are just existent to make the array homogenous.
        The will be filtered out when requesting neighbors of a Tile.

        Args:
            size (int): Size of the board

        Returns:
            np.ndarray: Graph representing the board
        """

        array = []
        for index in range(size * size):
            x = index // size
            y = index % size

            # Upper left corner
            if x == 0 and y == 0:
                array.append(
                    [
                        self._board[0, 1],
                        self._board[1, 0],
                        self._north,
                        self._west,
                        self._virtual_tile,
                        self._virtual_tile,
                    ]
                )
            # Upper right corner
            elif x == 0 and y == size - 1:
                array.append(
                    [
                        self._board[0, size - 2],
                        self._board[1, size - 2],
                        self._board[1][size - 2],
                        self._north,
                        self._east,
                        self._virtual_tile,
                    ]
                )
            # Lower left corner
            elif x == size - 1 and y == 0:
                array.append(
                    [
                        self._board[size - 1, 1],
                        self._board[size - 2, 0],
                        self._board[size - 2, 1],
                        self._south,
                        self._west,
                        self._virtual_tile,
                    ]
                )
            # Lower right corner
            elif x == size - 1 and y == size - 1:
                array.append(
                    [
                        self._board[size - 1, size - 2],
                        self._board[size - 2, size - 1],
                        self._south,
                        self._east,
                        self._virtual_tile,
                        self._virtual_tile,
                    ]
                )

            # Upper edge Nodes
            elif x == 0:
                array.append(
                    [
                        self._board[0, y - 1],
                        self._board[0, y + 1],
                        self._board[1, y - 1],
                        self._board[1, y],
                        self._north,
                        self._virtual_tile,
                    ]
                )
            # Lower edge Nodes
            elif x == size - 1:
                array.append(
                    [
                        self._board[size - 1, y - 1],
                        self._board[size - 1, y + 1],
                        self._board[size - 2, y],
                        self._board[size - 2, y + 1],
                        self._south,
                        self._virtual_tile,
                    ]
                )
            # Left edge Nodes
            elif y == 0:
                array.append(
                    [
                        self._board[x - 1, 0],
                        self._board[x + 1, 0],
                        self._board[x - 1, 1],
                        self._board[x, 1],
                        self._west,
                        self._virtual_tile,
                    ]
                )
            # Right edge Nodes
            elif y == size - 1:
                array.append(
                    [
                        self._board[x - 1, size - 1],
                        self._board[x + 1, size - 1],
                        self._board[x - 1, size - 2],
                        self._board[x, size - 2],
                        self._east,
                        self._virtual_tile,
                    ]
                )
            # Center Node
            else:
                array.append(
                    [
                        self._board[x, y - 1],
                        self._board[x, y + 1],
                        self._board[x - 1, y],
                        self._board[x - 1, y + 1],
                        self._board[x + 1, y],
                        self._board[x + 1, y - 1],
                    ]
                )

        assert len(array) == size * size

        return np.array(array)

    def get_neighbors(self, tile: Tile, player: Player | None = None) -> np.array:
        """Method to get the neighbors of a Tile

        Args:
            tile (Tile): Tile for which the neighbors should be returned

        Returns:
            np.array: Array of Tiles which are neighbors of the given Tile
        """
        index = tile.x * self._size + tile.y

        neighbor_tiles = self._graph[index]
        if player:
            return np.array(
                [
                    neighbor_tile
                    for neighbor_tile in neighbor_tiles
                    if neighbor_tile.player == player
                    and neighbor_tile != self._virtual_tile
                ]
            )
        else:
            return np.array(
                [
                    neighbor_tile
                    for neighbor_tile in neighbor_tiles
                    if neighbor_tile != self._virtual_tile
                ]
            )

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
        elif self._board[x, y].player == Player.EMPTY and player != Player.EMPTY:
            self._board[x, y].player = player
            return True
        else:
            return False

    def _start_game():
        pass

    def _game_loop():
        pass

    def _ai_move():
        pass

    def pi_rule():
        pass

    def _undo_move(self, x: int, y: int) -> None:
        """Method to undo a move on the board.

        Needed for fast and efficient simulation of Games

        Args:
            x (int): X coordinate of the Tile on the board.
            y (int): Y coordinate of the Tile on the board.
        """
        self._board[x, y].player = Player.EMPTY

    def _dfs(
        self, current_node: Tile, end_node: Tile, visited: set[Tile], player: Player
    ) -> bool:
        neighbors = hex.get_neighbors(current_node, player)

        if current_node == end_node:
            return True

        else:
            for neighbor in neighbors:
                if neighbor not in visited and self._dfs(
                    neighbor, end_node, visited, player
                ):
                    return True
                else:
                    continue

            return False

    def check_winner(self) -> Player | bool:
        if self._round < 2 * self._size - 1:
            return False
        elif self._dfs(self._north, self._south, set(), player=Player.WHITE):
            return Player.WHITE
        elif self._dfs(self._west, self._east, set(), player=Player.BLACK):
            return Player.BLACK


cli = CL_Interface()
hex = Hex(11, cli, cli)
hex.print_board()
