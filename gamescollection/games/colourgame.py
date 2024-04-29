"""
Implementation of MasterCode
"""

from enum import Enum
from random import choice, shuffle


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
        in_interface,
        out_interface,
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
        """Create solution which needs to be guessed based on number_colours

        Args might be potential modifiers for the solution like only unique colours etc...

        Args:
            unique_colours: Bool to determin if the colours selected for the solution should be unique or not

        Returns:
            List of colours which represents the solution which needs to be guessed
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

    def _cli_input(self) -> list[Colour]:
        """Input logic to play the game using the CLI

        Returns:
            List of Colours representing one guess
        """
        user_input = input()
        guess = user_input.split(",")
        if len(guess) != self._number_colours:
            print(
                f"Expected a guess with {self._number_colours} colours, got {len(guess)}. \n Retry."
            )
            self._cli_input()
        else:
            try:
                colour_guess = [Colour[colour.replace(" ", "")] for colour in guess]
            except KeyError:
                print("Please check the spelling of the colours and retry.")
                return self._cli_input()
            return colour_guess

    def out(self, try_n: int) -> None:
        """Output logic to play the game using the CLI

        In first round output an initial string, after this output structured view

        Args:
            try_n: Number of the current try

        Returns:
            None

        """
        colour_string = ", ".join(str(colour.name) for colour in self._colours)

        message = f"Number of Positions: {self._number_colours} \n Colours Available: {colour_string}\n Please seperate the Colours with ','. \n Please input {try_n + 1}. guess: "

        self._out_interface.out(message)

    def _game_loop(self) -> None:
        """Main game loop

        Get user Input, Output the

        Args:

        """

        # Get guess
        for try_n in range(self._tries):
            self._cli_out(try_n)
            guess = self._cli_input()
            self._guesses.append(guess)
            evaluation = []

            # Evaluate Guess
            for index, colour in enumerate(guess):
                # Check if correct position:
                if colour == self._solution[index]:
                    evaluation.append("Correct Position")
                elif colour in self._solution:
                    # TODO: FIX logic -> Curretly it does not count and evaluate the correct colour correctly...
                    evaluation.append("Correct Colour")
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
                for i in range(try_n + 1):
                    print(
                        f"Guess {i}: \n {','.join(colour.value for colour in self._guesses[i])} \n {self._evaluations[i]}"
                    )

        print(f"The solution was: \n {self._solution}")
