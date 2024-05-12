"""
Implementation of MasterCode
"""

from enum import Enum
from random import choice, shuffle
from copy import deepcopy


from custom_io.classes import CL_Interface, IO_Interface


class Colour(Enum):
    """Colour Implementation"""

    Yellow = 0
    Red = 1
    Green = 2
    Blue = 3
    Orange = 4
    Pink = 5
    Purple = 6


class UniqueSolutionError(Exception):
    """Can't produce a unique solution if there are less colours than spots"""

    pass


class ColorGame:
    """
    MasterCode Game Implementation
    """

    def __init__(
        self,
        fields: int,
        number_colours: int,
        tries: int,
        in_interface: IO_Interface,
        out_interface: IO_Interface,
        *,
        unique_colours: bool = False,
    ) -> None:
        """_summary_

        Args:
            fields (int): Number of Fields which need to be guessed
            number_colours (int): Number of Colours from which the solution can be picked
            tries (int): Number of tries the user has to guess the solution
            in_interface (_type_): Interface to get input from the user
            out_interface (_type_): Interface to output the game state to the user
            unique_colours (bool, optional): Game Setting, if colours should be unique. Defaults to False.
        """
        self._colours = list(Colour)[0:number_colours]
        self._number_colours = fields
        self._tries = tries
        self._in_interface = in_interface
        self._out_interface = out_interface
        self._guesses = []
        self._evaluations = []
        self._solution = self._generate_solution(unique_colours)
        self._game_loop()

    def _generate_solution(self, unique_colours: bool = False) -> list[Colour]:
        """Create solution which needs to be guessed based on number_colours and unique_colours.

        Args:
            unique_colours (bool, optional): If the colours should be unique. Defaults to False.

        Returns:
            list[Colour]: List of Colours which need to be guessed

        Raises:
            UniqueSolutionError: If unique_colours is True and the number of colours is less than the number of fields
        """
        # Create solution
        if unique_colours & self._number_colours <= len(self._colours):
            solution = []
            for _ in range(self._number_colours):
                colour = choice(self._colours)
                while colour in solution:
                    colour = choice(self._colours)

                solution.append(colour)

            assert len(solution) == self._number_colours

            return solution

        # Raise error to handle infinite loop case

        elif unique_colours:
            raise UniqueSolutionError

        # Create Solution with different conditions
        else:
            return [choice(self._colours) for _ in range(self._number_colours)]

    def _game_loop(self) -> None:
        """Main game loop for MasterCode"""

        # Get guess
        for try_n in range(self._tries):
            self._out_interface.out(f"Tries left: {self._tries - try_n}")
            self._out_interface.out(
                f"Colours: {','.join(colour.name for colour in self._colours)}"
            )

            for guess in self._guesses:
                self._out_interface.out(
                    f"Guess: {','.join(colour.value for colour in guess)}"
                )
                self._out_interface.out(
                    f"Evaluation: {','.join(result for result in self._evaluations)}"
                )

            self._out_interface.out("Please enter your guess:")
            guess = self._in_interface.inp()
            self._guesses.append(guess)
            evaluation = []
            temp_solution = deepcopy(self._solution)

            # Evaluate Guess
            for index, colour in enumerate(guess):
                # Check if correct position:
                if colour == self._solution[index]:
                    evaluation.append("Correct Position")
                elif colour in self._solution:
                    evaluation.append("Correct Colour")
                    temp_solution.remove(colour)
                else:
                    continue

            shuffle(evaluation)
            self._evaluations.append(evaluation)
            if evaluation is not None and all(
                result == "Correct Position" for result in evaluation
            ):
                print("Winner Winner Chicken Dinner!")
                break
            else:
                print("Try again")

        print("Game Over!")
        print(f"The solution was: \n {self._solution}")
