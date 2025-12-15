""" This module defines the BookManager class for managing books in the library system."""

from models.Book import Book


class BookManager:
    """BookManager class that manages all book operations."""

    def __init__(self, storage):
        """Initialize BookManager with a storage engine."""
        self.storage = storage

    def add_book(self, title, author, isbn, published_date, total_copies):
        """Add a new book to the library."""
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            published_date=published_date,
            available_copies=total_copies,
            total_copies=total_copies
        )
        self.storage.new(book)
        self.storage.save()
        return book

    def get_all_books(self):
        """Return all books in the library."""
        return self.storage.all(Book)

    def get_book_by_id(self, book_id):
        """Get a specific book by its ID."""
        books = self.get_all_books()
        key = f"Book.{book_id}"
        return books.get(key)

    def get_available_books(self):
        """Return only books with available copies."""
        books = self.get_all_books()
        return {key: book for key, book in books.items() if book.available_copies > 0}

    def update_available_copies(self, book_id, change):
        """Update the available copies of a book (positive to add, negative to subtract)."""
        book = self.get_book_by_id(book_id)
        if book:
            book.available_copies += change
            book.updated_at = __import__('datetime').datetime.now()
            self.storage.save()
            return book
        return None

    def delete_book(self, book_id):
        """Delete a book from the library."""
        books = self.get_all_books()
        key = f"Book.{book_id}"
        if key in books:
            del books[key]
            self.storage.save()
            return True
        return False
