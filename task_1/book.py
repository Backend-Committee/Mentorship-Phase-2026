class Book:
    # TODO: Use __slots__ to be more memory-efficient
    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        pub_date: int,
    ) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.pub_date: int = pub_date

    def update(self, title=None, author=None, pub_date=None):
        if title:
            self.title = title
        if author:
            self.author = author
        if pub_date:
            self.pub_date = pub_date

    def serialize(self) -> dict:
        return {"title": self.title, "author": self.author, "pub_date": self.pub_date}

    def __str__(self):
        return f"Book id: {self.id}\ntitle: {self.title}\nauthor: {self.author}\npub_date: {self.pub_date}"
