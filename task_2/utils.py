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
