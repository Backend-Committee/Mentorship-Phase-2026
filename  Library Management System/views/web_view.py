"""Web/JSON Views for REST API and web applications."""

import json
from views.formatters import BookFormatter, UserFormatter, TransactionFormatter


class WebBookView:
    """View class for providing book data in JSON format for web/API."""

    @staticmethod
    def get_books_json(books):
        """Get all books as JSON."""
        formatted = BookFormatter.format_books(books)
        return {
            "status": "success",
            "data": formatted,
            "count": len(formatted)
        }

    @staticmethod
    def get_book_json(book):
        """Get a single book as JSON."""
        formatted = BookFormatter.format_book(book)
        return {
            "status": "success",
            "data": formatted
        }

    @staticmethod
    def format_response(success, message, data=None):
        """Format a standard API response."""
        response = {
            "status": "success" if success else "error",
            "message": message
        }
        if data:
            response["data"] = data
        return response


class WebUserView:
    """View class for providing user data in JSON format for web/API."""

    @staticmethod
    def get_users_json(users):
        """Get all users as JSON."""
        formatted = UserFormatter.format_users(users)
        return {
            "status": "success",
            "data": formatted,
            "count": len(formatted)
        }

    @staticmethod
    def get_user_json(user):
        """Get a single user as JSON."""
        formatted = UserFormatter.format_user(user)
        return {
            "status": "success",
            "data": formatted
        }

    @staticmethod
    def format_response(success, message, data=None):
        """Format a standard API response."""
        response = {
            "status": "success" if success else "error",
            "message": message
        }
        if data:
            response["data"] = data
        return response


class WebTransactionView:
    """View class for providing transaction data in JSON format for web/API."""

    @staticmethod
    def get_transactions_json(transactions):
        """Get all transactions as JSON."""
        formatted = TransactionFormatter.format_transactions(transactions)
        return {
            "status": "success",
            "data": formatted,
            "count": len(formatted)
        }

    @staticmethod
    def get_transaction_json(trans):
        """Get a single transaction as JSON."""
        formatted = TransactionFormatter.format_transaction(trans)
        return {
            "status": "success",
            "data": formatted
        }

    @staticmethod
    def format_response(success, message, data=None):
        """Format a standard API response."""
        response = {
            "status": "success" if success else "error",
            "message": message
        }
        if data:
            response["data"] = data
        return response
