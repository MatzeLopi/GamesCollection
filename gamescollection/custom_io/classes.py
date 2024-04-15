from typing import Callable


class CommandLineIO:
    """
    A class that provides input/output functionality for command line interfaces.
    """

    def out(self, message: str):
        """
        Prints the given message to the console.

        Args:
            message (str): The message to be printed.
        """
        print(message)

    def in_(self, message, filter: Callable = None):
        """
        Reads user input from the console.

        Args:
            message: The prompt message to be displayed.
            filter (Callable, optional): A function to filter the user input. Defaults to None.

        Returns:
            str: The user input.
        """
        return filter(input(message)) if filter else input(message)


class RESTIO:
    """Class to handle REST Interactions"""

    pass


test = CommandLineIO()

test.out("Hello World")

print(test.in_("Enter your name: "))
