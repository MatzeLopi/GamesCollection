# Add parent directory to the path
from sys import path as syspath
from os import path as ospath

current_dir = ospath.dirname(ospath.abspath(__file__))
syspath.append(current_dir)

# Custom imports
import games
import games.gameofhex
from custom_io import classes


def main():
    input_interface: classes.IO_Interface | None = None
    output_interface: classes.IO_Interface | None = None

    print(f"Welcome to the gamescollection package!")
    print(f"Please specify the input interface you want to use:")
    print(f"1. Command Line Interface")
    print(f"2. REST Interface")
    print(f"3. Exit")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            print("You have selected Command Line Interface")
            input_interface = classes.CL_Interface()
            break
        elif choice == "2":
            print("You have selected REST Interface")
            input_interface = classes.REST_Interface()
            break
        elif choice == "3":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please try again.")

    print(f"Please specify the output interface you want to use:")
    print(f"1. Command Line Interface")
    print(f"2. REST Interface")
    print(f"3. Exit")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            print("You have selected Command Line Interface")
            output_interface = classes.CL_Interface()
            break
        elif choice == "2":
            print("You have selected REST Interface")
            output_interface = classes.REST_Interface()
            break
        elif choice == "3":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please try again.")

    assert (
        input_interface is not None and output_interface is not None
    ), "Input and Output interfaces must be selected."

    print(f"Input Interface: {input_interface}")
    print(f"Output Interface: {output_interface}")

    print("Please select the Game you want to play:")

    print("1. Master Code")
    print("2. Game of Hex")
    print("3. Exit")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":

            print("You have selected Master Code")

            print("Please enter the number of colours (max. 7):")
            number_colours = int(input("Enter the number of colours: "))
            while number_colours > 7 or number_colours < 1:
                print("Invalid number of colours. Please try again.")
                number_colours = int(input("Enter the number of colours: "))

            print("Please enter the number of tries:")
            tries = int(input("Enter the number of tries: "))
            while tries < 1:
                print("Invalid number of tries. Please try again.")
                tries = int(input("Enter the number of tries: "))

            print("Please enter the length of the code:")
            code_length = int(input("Enter the length of the code: "))
            while code_length < 1:
                print("Invalid code length. Please try again.")
                code_length = int(input("Enter the length of the code: "))

            game = games.colourgame.ColorGame(
                code_length,
                number_colours,
                tries,
                in_interface=input_interface,
                out_interface=output_interface,
            )
            exit()
        elif choice == "2":

            print("You have selected Game of Hex")

            print("Please enter the size of the board:")
            size = int(input("Enter the size: "))
            while size < 1:
                print("Invalid board size. Please try again.")
                size = int(input("Enter the size: "))

            game = games.gameofhex.Hex(
                size,
                input_interface,
                output_interface,
            )
            break
        elif choice == "3":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
