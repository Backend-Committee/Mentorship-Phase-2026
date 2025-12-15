"""Data formatting utilities for consistent output across different UI implementations."""


class BookFormatter:
    """Formatter for book data."""

    @staticmethod
    def format_books(books):
        """
        Format books data for display.
        
        Returns:
            dict with formatted data suitable for any UI (CLI, Web, GUI)
        """
        formatted_books = []
        for key, book in books.items():
            formatted_books.append({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "published_date": book.published_date,
                "available_copies": book.available_copies,
                "total_copies": book.total_copies,
                "created_at": book.created_at.isoformat() if hasattr(book.created_at, 'isoformat') else str(book.created_at),
                "updated_at": book.updated_at.isoformat() if hasattr(book.updated_at, 'isoformat') else str(book.updated_at),
            })
        return formatted_books

    @staticmethod
    def format_book(book):
        """Format a single book object."""
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "published_date": book.published_date,
            "available_copies": book.available_copies,
            "total_copies": book.total_copies,
        }


class UserFormatter:
    """Formatter for user data."""

    @staticmethod
    def format_users(users):
        """Format users data for display."""
        formatted_users = []
        for key, user in users.items():
            formatted_users.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "membership_date": user.membership_date,
                "active": user.active,
                "status": "Active" if user.active else "Inactive",
                "created_at": user.created_at.isoformat() if hasattr(user.created_at, 'isoformat') else str(user.created_at),
                "updated_at": user.updated_at.isoformat() if hasattr(user.updated_at, 'isoformat') else str(user.updated_at),
            })
        return formatted_users

    @staticmethod
    def format_user(user):
        """Format a single user object."""
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "membership_date": user.membership_date,
            "active": user.active,
            "status": "Active" if user.active else "Inactive",
        }


class TransactionFormatter:
    """Formatter for transaction data."""

    @staticmethod
    def format_transactions(transactions):
        """Format transactions data for display."""
        formatted_transactions = []
        for key, trans in transactions.items():
            formatted_transactions.append({
                "id": trans.id,
                "user_id": trans.user_id,
                "book_id": trans.book_id,
                "transaction_type": trans.transaction_type,
                "transaction_date": trans.transaction_date,
                "return_date": trans.return_date,
                "status": trans.status,
                "created_at": trans.created_at.isoformat() if hasattr(trans.created_at, 'isoformat') else str(trans.created_at),
                "updated_at": trans.updated_at.isoformat() if hasattr(trans.updated_at, 'isoformat') else str(trans.updated_at),
            })
        return formatted_transactions

    @staticmethod
    def format_transaction(trans):
        """Format a single transaction object."""
        return {
            "id": trans.id,
            "user_id": trans.user_id,
            "book_id": trans.book_id,
            "transaction_type": trans.transaction_type,
            "transaction_date": trans.transaction_date,
            "return_date": trans.return_date,
            "status": trans.status,
        }
