from typing import List

from features.account.IAccountRepo import IAccountRepo
from features.account.model import Account


class AccountService:
    def __init__(self, account_repo: IAccountRepo):
        self.account_repo = account_repo

    def create_account(self, title: str, user_id: int, balance: int = 0) -> Account:
        if not user_id:
            raise ValueError("user_id must be provided")
        return self.account_repo.create_account(
            title=title, balance=balance, user_id=user_id
        )

    def get_all_user_accounts(self, user_id: int) -> List[Account]:
        accounts = self.account_repo.get_all_user_accounts(user_id)
        return accounts

    def get_account(self, id: int) -> Account:
        account = self.account_repo.get_account(id)
        if account is None:
            raise LookupError(f"Account with id {id} not found.")
        return account

    def update_account(self, id: int, data: dict) -> Account:
        self.get_account(id)  # Will raise LookupError if the id is not valid

        if "title" in data:
            if not data["title"] or not data["title"].strip():
                raise ValueError("Account title cannot be empty.")
            data["title"] = data["title"].strip()

        updated = self.account_repo.update_account(id, data)
        if updated is None:
            raise LookupError(f"Account with id {id} not found.")
        return updated

    def delete_user(self, id: int) -> None:
        self.get_account(id)

        deleted = self.account_repo.delete_account(id)
        if not deleted:
            raise LookupError(f"User with id {id} not found.")

    def add_transaction(self, id: int, tx_type, amount: int):
        self.get_account(id)

        if int(amount) <= 0:
            raise ValueError("Amount must be positive number")
        return self.account_repo.add_transaction(id, tx_type, amount)

        # id INTEGER PRIMARY KEY AUTOINCREMENT,
        # description TEXT,
        # src_bank_account_id INTEGER NOT NULL,
        # dst_bank_account_id INTEGER NOT NULL,
        # amount REAL NOT NULL,
        # FOREIGN KEY (src_bank_account_id) REFERENCES BankAcc(id),
        # FOREIGN KEY (dst_bank_account_id) REFERENCES BankAcc(id)

    def add_transfer(
        self, src_id: int, dst_id: int, amount: int, description: str = "Transfer!"
    ):
        self.get_account(src_id)
        self.get_account(dst_id)

        if int(amount) <= 0:
            raise ValueError("Amount must be positive number")
        return self.account_repo.add_transfer(src_id, dst_id, amount, description)
