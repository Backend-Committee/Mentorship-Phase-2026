class User:
    # TODO: Use __slots__ to be more memory-efficient
    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        borrowings: list[int]
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.email: str = email
        self.borrowings: list[int] = borrowings

    def update(self, name=None, email=None, borrowings=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if borrowings:
            self.borrowings = borrowings

    def serialize(self) -> dict:
        return {"name": self.name, "email": self.email, "borrowings": self.borrowings}

    def __str__(self):
        return f"User id: {self.id}\nname: {self.name}\nemail: {self.email}"
