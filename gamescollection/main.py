from custom_io import classes
import games
import games.gameofhex


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
            print("Not implemented yet")
            exit()
        elif choice == "2":
            print("You have selected Game of Hex")
            print("Please enter the size of the board:")
            size = int(input("Enter the size: "))
            game = games.gameofhex.Hex(size, input_interface, output_interface)
            break
        elif choice == "3":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
