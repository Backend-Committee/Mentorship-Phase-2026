"""GUI Views for Tkinter and other GUI frameworks."""

from views.formatters import BookFormatter, UserFormatter, TransactionFormatter


class GUIBookView:
    """View class for providing book data for GUI applications."""

    @staticmethod
    def get_books_for_table(books):
        """
        Get books data in format suitable for GUI tables.
        
        Returns:
            list of tuples: (id, title, author, isbn, available, total)
        """
        rows = []
        for key, book in books.items():
            rows.append((
                book.id,
                book.title,
                book.author,
                book.isbn,
                book.available_copies,
                book.total_copies
            ))
        return rows

    @staticmethod
    def get_book_details(book):
        """Get book details as dictionary for GUI forms."""
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "published_date": book.published_date,
            "available": book.available_copies,
            "total": book.total_copies,
        }


class GUIUserView:
    """View class for providing user data for GUI applications."""

    @staticmethod
    def get_users_for_table(users):
        """
        Get users data in format suitable for GUI tables.
        
        Returns:
            list of tuples: (id, name, email, status)
        """
        rows = []
        for key, user in users.items():
            status = "Active" if user.active else "Inactive"
            rows.append((
                user.id,
                user.name,
                user.email,
                status
            ))
        return rows

    @staticmethod
    def get_user_details(user):
        """Get user details as dictionary for GUI forms."""
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "membership_date": user.membership_date,
            "active": user.active,
        }


class GUITransactionView:
    """View class for providing transaction data for GUI applications."""

    @staticmethod
    def get_transactions_for_table(transactions):
        """
        Get transactions data in format suitable for GUI tables.
        
        Returns:
            list of tuples: (id, user_id, book_id, type, date, status)
        """
        rows = []
        for key, trans in transactions.items():
            rows.append((
                trans.id,
                trans.user_id,
                trans.book_id,
                trans.transaction_type,
                trans.transaction_date,
                trans.status
            ))
        return rows

    @staticmethod
    def get_transaction_details(trans):
        """Get transaction details as dictionary for GUI forms."""
        return {
            "id": trans.id,
            "user_id": trans.user_id,
            "book_id": trans.book_id,
            "type": trans.transaction_type,
            "transaction_date": trans.transaction_date,
            "return_date": trans.return_date,
            "status": trans.status,
        }
