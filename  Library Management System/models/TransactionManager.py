""" This module defines the TransactionManager class for managing transactions in the library system."""

from models.Transaction import Transaction
from datetime import datetime


class TransactionManager:
    """TransactionManager class that manages borrowing and returning of books."""

    def __init__(self, storage, book_manager, user_manager):
        """Initialize TransactionManager with storage and manager instances."""
        self.storage = storage
        self.book_manager = book_manager
        self.user_manager = user_manager

    def borrow_book(self, user_id, book_id):
        """Record a book borrowing transaction."""
        user = self.user_manager.get_user_by_id(user_id)
        if not user:
            return {"success": False, "message": "User not found"}

        if not user.active:
            return {"success": False, "message": "User account is inactive"}

        book = self.book_manager.get_book_by_id(book_id)
        if not book:
            return {"success": False, "message": "Book not found"}

        if book.available_copies <= 0:
            return {"success": False, "message": "Book is not available"}

        # Create transaction record
        transaction = Transaction(
            user_id=user_id,
            book_id=book_id,
            transaction_type="borrow",
            transaction_date=datetime.now().isoformat(),
            status="active"
        )
        
        self.storage.new(transaction)
        
        # Reduce available copies
        self.book_manager.update_available_copies(book_id, -1)
        
        return {"success": True, "message": f"Book '{book.title}' borrowed successfully", "transaction_id": transaction.id}

    def return_book(self, user_id, book_id):
        """Record a book return transaction."""
        user = self.user_manager.get_user_by_id(user_id)
        if not user:
            return {"success": False, "message": "User not found"}

        book = self.book_manager.get_book_by_id(book_id)
        if not book:
            return {"success": False, "message": "Book not found"}

        # Find the active borrow transaction
        transactions = self.storage.all(Transaction)
        borrow_transaction = None
        
        for key, trans in transactions.items():
            if (trans.user_id == user_id and trans.book_id == book_id and 
                trans.transaction_type == "borrow" and trans.status == "active"):
                borrow_transaction = trans
                break

        if not borrow_transaction:
            return {"success": False, "message": "No active borrow record found for this user and book"}

        # Update the borrow transaction
        borrow_transaction.status = "completed"
        borrow_transaction.return_date = datetime.now().isoformat()
        borrow_transaction.updated_at = datetime.now()

        # Create a return transaction
        return_transaction = Transaction(
            user_id=user_id,
            book_id=book_id,
            transaction_type="return",
            transaction_date=datetime.now().isoformat(),
            status="completed"
        )

        self.storage.new(return_transaction)
        self.storage.save()

        # Increase available copies
        self.book_manager.update_available_copies(book_id, 1)

        return {"success": True, "message": f"Book '{book.title}' returned successfully"}

    def get_user_borrowed_books(self, user_id):
        """Get all books currently borrowed by a user."""
        transactions = self.storage.all(Transaction)
        borrowed_books = {}
        
        for key, trans in transactions.items():
            if (trans.user_id == user_id and trans.transaction_type == "borrow" 
                and trans.status == "active"):
                book = self.book_manager.get_book_by_id(trans.book_id)
                if book:
                    borrowed_books[key] = {
                        "book": book,
                        "borrow_date": trans.transaction_date,
                        "transaction_id": trans.id
                    }
        
        return borrowed_books

    def get_all_transactions(self):
        """Get all transactions."""
        return self.storage.all(Transaction)
