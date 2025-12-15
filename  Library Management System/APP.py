""" Library Management System - Main Application """

from models.engine.file_storage import FileStorage
from models.BookManager import BookManager
from models.UserManager import UserManager
from models.TransactionManager import TransactionManager
from views.cli_view import BookView, UserView, TransactionView
from datetime import datetime


class LibraryApp:
    """Main application class for the Library Management System."""

    def __init__(self):
        """Initialize the application."""
        self.storage = FileStorage()
        self.book_manager = BookManager(self.storage)
        self.user_manager = UserManager(self.storage)
        self.transaction_manager = TransactionManager(
            self.storage, self.book_manager, self.user_manager
        )
        # Initialize view layers
        self.book_view = BookView()
        self.user_view = UserView()
        self.transaction_view = TransactionView()

    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("LIBRARY MANAGEMENT SYSTEM ".center(60))
        print("="*60)
        print("\n1.  Add Book")
        print("2.  Add User")
        print("3.  Borrow Book")
        print("4.  Return Book")
        print("5.  Display Available Books")
        print("6.  Display All Books")
        print("7.  Display All Users")
        print("8.  Display My Borrowed Books")
        print("9.  Display All Transactions")
        print("10. Search Book by Title")
        print("11. User Borrowed History")
        print("0.  Exit")
        print("="*60)

    def add_book(self):
        """Add a new book to the library."""
        print("\n--- Add New Book ---")
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        isbn = input("Enter ISBN: ").strip()
        published_date = input("Enter published date (YYYY-MM-DD): ").strip()
        
        try:
            total_copies = int(input("Enter total copies: "))
            if total_copies <= 0:
                print("Total copies must be greater than 0")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        book = self.book_manager.add_book(
            title, author, isbn, published_date, total_copies
        )
        print(f"Book '{title}' added successfully! (ID: {book.id})")

    def add_user(self):
        """Add a new user to the library."""
        print("\n--- Add New User ---")
        name = input("Enter user name: ").strip()
        email = input("Enter email: ").strip()
        membership_date = datetime.now().strftime("%Y-%m-%d")

        user = self.user_manager.add_user(name, email, membership_date)
        print(f"User '{name}' added successfully! (ID: {user.id})")
        print(f"   Membership Date: {membership_date}")

    def borrow_book(self):
        """Borrow a book."""
        print("\n--- Borrow Book ---")
        user_id = input("Enter your User ID: ").strip()
        book_id = input("Enter Book ID to borrow: ").strip()

        result = self.transaction_manager.borrow_book(user_id, book_id)
        
        if result["success"]:
            print(f"{result['message']}")
        else:
            print(f"{result['message']}")

    def return_book(self):
        """Return a book."""
        print("\n--- Return Book ---")
        user_id = input("Enter your User ID: ").strip()
        book_id = input("Enter Book ID to return: ").strip()

        result = self.transaction_manager.return_book(user_id, book_id)
        
        if result["success"]:
            print(f"{result['message']}")
        else:
            print(f"{result['message']}")

    def display_available_books(self):
        """Display all available books."""
        print("\n--- Available Books ---")
        available_books = self.book_manager.get_available_books()
        self.book_view.display_books(available_books)

    def display_all_books(self):
        """Display all books in the library."""
        print("\n--- All Books in Library ---")
        all_books = self.book_manager.get_all_books()
        self.book_view.display_books(all_books)

    def display_all_users(self):
        """Display all users."""
        print("\n--- All Users ---")
        all_users = self.user_manager.get_all_users()
        self.user_view.display_users(all_users)

    def display_my_borrowed_books(self):
        """Display books borrowed by the current user."""
        print("\n--- My Borrowed Books ---")
        user_id = input("Enter your User ID: ").strip()
        
        borrowed_books = self.transaction_manager.get_user_borrowed_books(user_id)
        self.transaction_view.display_borrowed_books(borrowed_books)

    def display_all_transactions(self):
        """Display all transactions."""
        print("\n--- All Transactions ---")
        transactions = self.transaction_manager.get_all_transactions()
        self.transaction_view.display_transactions(transactions)

    def search_book_by_title(self):
        """Search for a book by title."""
        print("\n--- Search Book by Title ---")
        search_title = input("Enter book title to search: ").strip().lower()
        
        all_books = self.book_manager.get_all_books()
        results = {
            key: book for key, book in all_books.items()
            if search_title in book.title.lower()
        }

        if not results:
            print(f"No books found matching '{search_title}'")
            return

        print(f"\n Found {len(results)} book(s):")
        self.book_view.display_books(results)

    def user_borrowed_history(self):
        """Display borrowing history of a user."""
        print("\n--- User Borrowed History ---")
        user_id = input("Enter User ID: ").strip()
        
        user = self.user_manager.get_user_by_id(user_id)
        if not user:
            print("User not found")
            return

        transactions = self.transaction_manager.get_all_transactions()
        user_transactions = {
            key: trans for key, trans in transactions.items()
            if trans.user_id == user_id
        }

        if not user_transactions:
            print(f"No transactions found for user '{user.name}'")
            return

        print(f"\n Borrowing history for {user.name}:")
        self.transaction_view.display_transactions(user_transactions)

    def run(self):
        """Run the application."""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (0-11): ").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.add_user()
            elif choice == "3":
                self.borrow_book()
            elif choice == "4":
                self.return_book()
            elif choice == "5":
                self.display_available_books()
            elif choice == "6":
                self.display_all_books()
            elif choice == "7":
                self.display_all_users()
            elif choice == "8":
                self.display_my_borrowed_books()
            elif choice == "9":
                self.display_all_transactions()
            elif choice == "10":
                self.search_book_by_title()
            elif choice == "11":
                self.user_borrowed_history()
            elif choice == "0":
                print("\n Thank you for using Library Management System!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = LibraryApp()
    app.run()
