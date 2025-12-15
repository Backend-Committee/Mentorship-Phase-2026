"""CLI Views for Console/Terminal display."""

from views.formatters import BookFormatter, UserFormatter, TransactionFormatter


class BookView:
    """View class for displaying book data in CLI format."""

    @staticmethod
    def display_books(books):
        """Display books in a formatted table."""
        if not books:
            print("No books found.")
            return

        print("\n" + "="*100)
        print(f"{'Title':<30} {'Author':<20} {'ISBN':<15} {'Available':<10} {'Total':<10}")
        print("="*100)

        for key, book in books.items():
            print(f"{book.title:<30} {book.author:<20} {book.isbn:<15} {book.available_copies:<10} {book.total_copies:<10}")

        print("="*100 + "\n")

    @staticmethod
    def display_book(book):
        """Display a single book."""
        formatted = BookFormatter.format_book(book)
        print("\n" + "="*60)
        print(f"Book Details:")
        print("="*60)
        for key, value in formatted.items():
            print(f"{key.capitalize():<20}: {value}")
        print("="*60 + "\n")

    @staticmethod
    def display_books_json(books):
        """Return books data as JSON-friendly format."""
        return BookFormatter.format_books(books)


class UserView:
    """View class for displaying user data in CLI format."""

    @staticmethod
    def display_users(users):
        """Display users in a formatted table."""
        if not users:
            print("No users found.")
            return

        print("\n" + "="*80)
        print(f"{'Name':<25} {'Email':<30} {'Status':<10} {'Member Since':<15}")
        print("="*80)

        for key, user in users.items():
            status = "Active" if user.active else "Inactive"
            print(f"{user.name:<25} {user.email:<30} {status:<10} {user.membership_date:<15}")

        print("="*80 + "\n")

    @staticmethod
    def display_user(user):
        """Display a single user."""
        formatted = UserFormatter.format_user(user)
        print("\n" + "="*60)
        print(f"User Details:")
        print("="*60)
        for key, value in formatted.items():
            print(f"{key.capitalize():<20}: {value}")
        print("="*60 + "\n")

    @staticmethod
    def display_users_json(users):
        """Return users data as JSON-friendly format."""
        return UserFormatter.format_users(users)


class TransactionView:
    """View class for displaying transaction data in CLI format."""

    @staticmethod
    def display_transactions(transactions):
        """Display transactions in a formatted table."""
        if not transactions:
            print("No transactions found.")
            return

        print("\n" + "="*120)
        print(f"{'User ID':<15} {'Book ID':<15} {'Type':<10} {'Date':<20} {'Return Date':<20} {'Status':<12}")
        print("="*120)

        for key, trans in transactions.items():
            return_date = trans.return_date if trans.return_date else "N/A"
            print(f"{trans.user_id:<15} {trans.book_id:<15} {trans.transaction_type:<10} {trans.transaction_date:<20} {return_date:<20} {trans.status:<12}")

        print("="*120 + "\n")

    @staticmethod
    def display_transaction(trans):
        """Display a single transaction."""
        formatted = TransactionFormatter.format_transaction(trans)
        print("\n" + "="*60)
        print(f"Transaction Details:")
        print("="*60)
        for key, value in formatted.items():
            print(f"{key.capitalize():<20}: {value}")
        print("="*60 + "\n")

    @staticmethod
    def display_transactions_json(transactions):
        """Return transactions data as JSON-friendly format."""
        return TransactionFormatter.format_transactions(transactions)

    @staticmethod
    def display_borrowed_books(borrowed_books):
        """Display books borrowed by a user."""
        if not borrowed_books:
            print("No borrowed books found.")
            return

        print("\n" + "="*100)
        print(f"{'Title':<30} {'Author':<20} {'ISBN':<15} {'Borrow Date':<20}")
        print("="*100)

        for key, item in borrowed_books.items():
            book = item["book"]
            print(f"{book.title:<30} {book.author:<20} {book.isbn:<15} {item['borrow_date']:<20}")

        print("="*100 + "\n")
