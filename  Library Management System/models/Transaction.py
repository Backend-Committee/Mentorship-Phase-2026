""" This module defines the Transaction class representing a transaction in the library management system."""
from models.BaseModel import BaseModel

class Transaction(BaseModel):
    """Transaction class that represents a transaction in the library management system."""

    def __init__(self, *args, **kwargs):
        """Initialize a new Transaction instance."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', "")
        self.book_id = kwargs.get('book_id', "")
        self.transaction_type = kwargs.get('transaction_type', "")  # e.g., 'borrow' or 'return'
        self.transaction_date = kwargs.get('transaction_date', "")
        self.return_date = kwargs.get('return_date', "")
        self.status = kwargs.get('status', "active")  # e.g., 'active', 'completed'