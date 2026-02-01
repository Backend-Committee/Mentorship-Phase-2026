import sqlite3
from typing import List, Tuple

from features.account.IAccountRepo import IAccountRepo
from features.account.model import Account


class AccountRepo(IAccountRepo):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_account(self, title: str, balance: int, user_id: int) -> Account:
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO BankAcc (title, balance, user_id) VALUES (?, ?, ?)",
                (
                    title,
                    balance,
                    user_id,
                ),
            )
            return Account(
                id=cursor.lastrowid, title=title, balance=balance, user_id=user_id
            )

    def get_account(self, id: int) -> Account | None:
        cursor = self.conn.execute("SELECT * FROM BankAcc WHERE id = ?", (id,))
        row = cursor.fetchone()
        return Account.from_row(row) if row else None

    def update_account(self, id: int, data: dict) -> Account | None:
        allowed = {"title", "balance"}
        filtered = {k: v for k, v in data.items() if k in allowed}

        if not filtered:
            return self.get_account(id)

        set_clause = ", ".join(
            f"{'auth_id' if k == 'auth_id' else k} = ?" for k in filtered
        )
        values = list(filtered.values()) + [id]

        with self.conn:
            self.conn.execute(f"UPDATE BankAcc SET {set_clause} WHERE id = ?", values)
        return self.get_account(id)

    def delete_account(self, id: int) -> bool:
        with self.conn:
            cursor = self.conn.execute("DELETE FROM BankAcc WHERE id = ?", (id,))
            return cursor.rowcount > 0

    def get_all_user_accounts(self, user_id: int) -> list[Account]:
        cursor = self.conn.execute(
            "SELECT * FROM BankAcc WHERE user_id = ?", (user_id,)
        )
        rows = cursor.fetchall()

        accounts = []

        for row in rows:
            accounts.append(Account.from_row(row))

        return accounts

    def add_transaction(self, id, tx_type, amount) -> Account | None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO [Transaction] (amount, type, bank_account_id) VALUES (?, ?, ?)",
                (amount, tx_type, id),
            )

            if tx_type == "income":
                self.conn.execute(
                    "UPDATE BankAcc SET balance = balance + ? WHERE id = ?",
                    (amount, id),
                )
            else:
                self.conn.execute(
                    "UPDATE BankAcc SET balance = balance - ? WHERE id = ?",
                    (amount, id),
                )
        return self.get_account(id)

    def add_transfer(
        self, src_id: int, dst_id: int, amount: float, description: str
    ) -> tuple[Account, Account] | None:
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO Transfer (amount, src_bank_account_id, dst_bank_account_id, description)
                VALUES (?, ?, ?, ?)
                """,
                (amount, src_id, dst_id, description),
            )

            self.conn.execute(
                """
                UPDATE BankAcc
                SET balance = CASE
                    WHEN id = ? THEN balance - ?
                    WHEN id = ? THEN balance + ?
                END
                WHERE id IN (?, ?)
                """,
                (src_id, amount, dst_id, amount, src_id, dst_id),
            )

        return self.get_account(src_id), self.get_account(dst_id)

    def get_account_statement(self, account_id: int) -> list[str] | None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO [Transaction] (amount, type, bank_account_id) VALUES (?, ?, ?)",
                (amount, tx_type, id),
            )

            if tx_type == "income":
                self.conn.execute(
                    "UPDATE BankAcc SET balance = balance + ? WHERE id = ?",
                    (amount, id),
                )
            else:
                self.conn.execute(
                    "UPDATE BankAcc SET balance = balance - ? WHERE id = ?",
                    (amount, id),
                )
        return self.get_account(id)
