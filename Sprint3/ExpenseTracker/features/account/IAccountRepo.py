from abc import ABC, abstractmethod
from typing import List, Tuple

from features.account.model import Account


class IAccountRepo(ABC):
    @abstractmethod
    def create_account(self, title: str, balance: int, user_id: int) -> Account:
        """Create a new Account and return the created Account instance."""
        pass

    @abstractmethod
    def get_account(self, id: int) -> Account | None:
        """Fetch an Account by their ID. Returns None if not found."""
        pass

    @abstractmethod
    def update_account(self, id: int, data: dict) -> Account | None:
        """Update a Account's data by ID. Returns the updated Account, or None if not found."""
        pass

    @abstractmethod
    def delete_account(self, id: int) -> bool:
        """Delete an account by ID. Returns True if deleted, False if not found."""
        pass

    @abstractmethod
    def get_all_user_accounts(self, user_id: int) -> list[Account]:
        """Get All Accounts for a user"""
        pass

    @abstractmethod
    def add_transaction(self, id, tx_type, amount) -> Account | None:
        """Add a transaction income or expenes!"""
        pass

    @abstractmethod
    def add_transfer(
        self, src_id: int, dst_id: int, amount: float, description: str
    ) -> tuple[Account, Account] | None:
        """Add a Transfer"""
        pass

    @abstractmethod
    def get_account_statement(self, account_id: int) -> list[str] | None:
        """Get all account history"""
        pass
