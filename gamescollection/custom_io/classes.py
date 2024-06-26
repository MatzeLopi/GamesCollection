from typing import Callable


class IO_Interface:
    """Interface for Input/Output"""

    pass


class CL_Interface(IO_Interface):
    """
    A class that provides input/output functionality for command line.
    """

    def out(self, message: str):
        """
        Prints the given message to the console.

        Args:
            message (str): The message to be printed.
        """
        print(message)

    def inp(self, message: str | None = None, filter: Callable = None):
        """
        Reads user input from the console.

        Args:
            message: The prompt message to be displayed.
            filter (Callable, optional): A function to filter the user input. Defaults to None.

        Returns:
            str: The user input.
        """
        if message is None:
            return filter(input()) if filter else input()
        else:
            return filter(input(message)) if filter else input(message)


class REST_Interface(IO_Interface):
    """Class to provide input/output functionality for REST API"""

    def __init__(self) -> None:
        pass
