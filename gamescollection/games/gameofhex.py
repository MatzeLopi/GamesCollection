import random
import numpy as np
import itertools as it
from enum import Enum
from typing import TYPE_CHECKING
from sys import path
from os import path as ospath
from copy import deepcopy

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
        """Default constructor to initialize a Tile to a known state if no data is given."""
        self.x = -100
        self.y = -100
        self.player = Player.EMPTY

    def __init__(self, x: int, y: int, player: Player | None = None) -> None:
        """Initialize a Tile with given coordinates and player.

        Args:
            x (int): X coordinate of the Tile
            y (int): Y coordinate of the Tile
            player (Player, optional): Player who owns the Tile. Defaults to Player.EMPTY.
        """
        self.x = x
        self.y = y
        self.player = player if player else Player.EMPTY

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
    """A Game of Hex in python

    Attributes:
        size (int): Size of the board
        in_interface (IO_Interface): Interface to get User Input
        out_interface (IO_Interface): Interface to display output to the User
        round (int): Current round of the game
        player (Player): Human player
        ai (Player): AI against which the game is played
        current_player (Player): Player who is currently playing
        north (Tile): Special Tile for the north zone of the board
        south (Tile): Special Tile for the south zone of the board
        east (Tile): Special Tile for the east zone of the board
        west (Tile): Special Tile for the west zone of the board
        virtual_tile (Tile): Virtual Tile to make the array homogenous
        board (np.ndarray): Game board representation as a 2D array
        graph (np.ndarray): Graph representation of the board
    """

    def __init__(
        self,
        size: int,
        in_interface: IO_Interface,
        out_interface: IO_Interface,
        simulations: int = 200,
    ) -> None:
        """Initialize the Hex game based on the size of the board and the interfaces for input and output.

        Args:
            size (int): Size of the hex board
            in_interface (IO_Interface): Interface to get User Input
            out_interface (IO_Interface): Interface to display output to the User
        """
        # General attributes
        self._size = size
        self._in_interface = in_interface
        self._out_interface = out_interface
        self._simulations = simulations

        # Game state related attributes
        self._round = 0
        self._player: Player
        self._ai: Player
        self._current_player: Player
        self._winner: Player = Player.EMPTY

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

        self._start_game()

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

    def _get_neighbors(self, tile: Tile, player: Player | None = None) -> np.array:
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

    def _print_board(self) -> None:
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

    def _make_move(self, x: int, y: int, player: Player) -> bool:
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
            self._round += 1
            # Update the current player
            self._current_player = (
                self._ai if self._current_player == self._player else self._player
            )
            return True
        else:
            return False

    def _start_game(self) -> None:
        """Method to start the Game.

        Player can choose their color and the game loop is started.

        """
        self._out_interface.out("Welcome to Hex!")
        self._out_interface.out("Please select a color: X or O:")
        choice = self._in_interface.inp().lower()
        while choice != "x" and choice != "o":
            self._out_interface.out("Please select a valid color: X or O:")
            choice = self._in_interface.inp().lower()

        if choice == "x":
            self._player = Player.WHITE
            self._ai = Player.BLACK
        else:
            self._player = Player.BLACK
            self._ai = Player.WHITE

        self._current_player = (
            self._player if self._player == Player.WHITE else self._ai
        )
        self._out_interface.out("You are playing as: " + str(self._player))

        self._game_loop()

    def _human_move(self) -> None:
        """Logic to get input from Human to make move

        Will loop until a valid move is made.
        """

        while True:
            self._out_interface.out("Please make a move: x y")
            try:
                x, y = self._in_interface.inp().split(" ")
                x, y = int(x), int(y)

            except ValueError:
                continue
            else:

                if self._make_move(x, y, self._player):
                    break
                else:
                    self._out_interface.out("Invalid Move.")

    def _game_loop(self):
        if round == 1:
            self._pi_rule()

        while not self._check_winner():
            if self._current_player == self._player:
                self._human_move()
            else:
                self._ai_move()

            self._print_board()

        print(f"Player {self._winner} won!")

    def _get_legal_moves(self) -> list[Tile]:
        """Get Legal Moves on the board

        Returns:
            _type_: _description_
        """
        flattened_board = self._board.flatten()
        moves = [tile for tile in flattened_board if tile.player == Player.EMPTY]
        return moves

    def _ai_move(self):
        # Run Monte carlo simulations to find the best move
        best_score: int = -1 * int(1e9)
        best_move: Tile | None = None

        legal_moves: list[Tile] = self._get_legal_moves()

        for move in legal_moves:
            move_score: int = 0
            for _ in range(self._simulations):
                # Create Copy of the current game-state
                temp_game = deepcopy(self)

                temp_game._make_move(move.x, move.y, temp_game._current_player)

                while not temp_game._check_winner():
                    legal_moves = temp_game._get_legal_moves()
                    random_move = random.choice(legal_moves)
                    temp_game._make_move(
                        random_move.x, random_move.y, temp_game._current_player
                    )
                temp_game._print_board()
                if temp_game._winner == temp_game._ai:
                    move_score += 1
                else:
                    move_score -= 1
            print(move_score)
            if move_score > best_score:
                best_score = move_score
                best_move = move
        self._make_move(best_move.x, best_move.y, self._current_player)

    def pi_rule(self) -> None:
        """Implementation of the PI rule in the game to make it fair for both players."""
        assert self._round == 1

        if self._current_player == self._player:
            self._out_interface.out("Do you want to change your color? (y/n)")
            choice = self._in_interface.inp().lower()
            while choice != "y" and choice != "n":
                self._out_interface.out("Please select a valid option: y or n")
                choice = self._in_interface.inp().lower()

            if choice == "y":
                self._player, self._ai = self._ai, self._player
            else:
                pass
        else:
            if random.choice([True, False]):
                self._player, self._ai = self._ai, self._player
            else:
                pass

    def _undo_move(self, x: int, y: int) -> None:
        """Method to undo a move on the board.

        Needed for fast and efficient simulation of Games

        Args:
            x (int): X coordinate of the Tile on the board.
            y (int): Y coordinate of the Tile on the board.
        """
        self._board[x, y].player = Player.EMPTY
        self._round -= 1

    def _dfs(
        self, current_node: Tile, end_node: Tile, visited: set[Tile], player: Player
    ) -> bool:
        """Depth First Search to check if there is a path from the current_node to the end_node

        Args:
            current_node (Tile): Current node in the search
            end_node (Tile): End node of the search
            visited (set[Tile]): Set which holds the nodes which were visited
            player (Player): Player to which the node needs to belong to be able to walk the path

        Returns:
            bool: True if there is a path from current_node to end_node else False
        """
        neighbors = self._get_neighbors(current_node, player)

        assert all(tile.player == player for tile in neighbors), "Player mismatch"
        assert player != Player.EMPTY, "Player can't be EMPTY"

        if current_node == end_node:
            return True

        else:
            visited.add(current_node)

            for neighbor in neighbors:
                if neighbor not in visited and self._dfs(
                    neighbor, end_node, visited, player
                ):
                    return True
                else:
                    continue

            return False

    def _check_winner(self) -> Player | bool:
        """Method to check if there is a winner in the game.

        Starts after the 2 * size - 1 round, since before that no player can win.

        Returns:
            Player | bool: Player who won the game or False if there is no winner yet.
        """

        if self._dfs(self._north, self._south, set(), player=Player.WHITE):
            self._winner = Player.WHITE
            return True
        elif self._dfs(self._west, self._east, set(), player=Player.BLACK):
            self._winner = Player.BLACK
            return True
        else:
            return False


game = Hex(5, CL_Interface(), CL_Interface())
