from sys import stderr


def get_opt(start, end) -> int:
    while True:
        try:
            opt = int(input("> "))
        except ValueError:
            ...
        else:
            if opt >= start and opt <= end:
                return opt

        print("This is not a valid option, please try again!", file=stderr)
        print()

def get_int(prompt) -> int:
    while True:
        try:
            opt = int(input(prompt))
            return opt
        except ValueError:
            print("Please enter a valid integer.", file=stderr)
            print()
            