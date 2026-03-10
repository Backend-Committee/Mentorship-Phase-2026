class Shape:
    def __init__(self): ...

    def get_input(self): ...

    def calculate_area(self): ...

    def calculate_perimeter(self): ...

    def __str__(self):
        """This should return ASCII art representation of the shape"""


class Rectangle(Shape):
    def __init__(self):
        self.length = 0
        self.height = 0

    def get_input(self):
        try:
            self.length = int(input("Enter the rectangle length: "))
            self.height = int(input("Enter the rectangle height: "))

            if self.length <= 0 or self.height <= 0:
                raise ValueError("Length and height must be positive")
        except ValueError as e:
            print(f"Invalid input: {e}")
            self.get_input()

    def calculate_area(self):
        return self.length * self.height

    def calculate_perimeter(self):
        return 2 * (self.length + self.height)

    def __str__(self):
        top_bottom = ("-  " * (self.length + 1)).rstrip()
        middle = "-" + " " * (len(top_bottom) - 2) + "-"
        lines = [top_bottom]
        lines.extend([middle] * (self.height - 1))
        lines.append(top_bottom)
        return "\n".join(lines)


class Square(Rectangle):
    def __init__(self):
        super().__init__()

    def get_input(self):
        try:
            side = int(input("Enter square side length: "))

            if side <= 0:
                raise ValueError("Side length must be positive")

            self.length = side
            self.height = side
        except ValueError as e:
            print(f"Invalid input: {e}")
            self.get_input()


def main():
    rectangle = Rectangle()
    rectangle.get_input()

    print(f"\nThe area of the rectangle is {rectangle.calculate_area()}")
    print(f"The perimeter of the rectangle is {rectangle.calculate_perimeter()}")
    print("\nImage:")
    print(rectangle)

    print()

    square = Square()
    square.get_input()

    print(f"\nThe area of the square is {square.calculate_area()}")
    print(f"The perimeter of the square is {square.calculate_perimeter()}")
    print("\nImage:")
    print(square)


if __name__ == "__main__":
    main()
