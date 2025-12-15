""" This module defines the Book class representing a book in the library management system."""

from models.BaseModel import BaseModel

class Book(BaseModel):
    """Book class that represents a book in the library management system."""

    def __init__(self, *args, **kwargs):
        """Initialize a new Book instance."""
        super().__init__(*args, **kwargs)
        self.title = kwargs.get('title', "")
        self.author = kwargs.get('author', "")
        self.isbn = kwargs.get('isbn', "")
        self.published_date = kwargs.get('published_date', "")
        self.available_copies = kwargs.get('available_copies', 0)
        self.total_copies = kwargs.get('total_copies', 0)
        