from dataclasses import dataclass


@dataclass
class Account:
    """Represents the Accounts tables - linked to user table"""

    id: int
    title: str
    balance: float
    user_id: int  # F.K

    @classmethod
    def from_row(cls, row) -> "Account":
        """Hydrate a Account instance from a sqlite3.Row object."""
        return cls(
            id=row["id"],
            title=row["title"],
            user_id=row["user_id"],
            balance=row["balance"],
        )

    def __str__(self) -> str:
        balance_str = f"${self.balance:,.2f}"
        id_line = f"{self.title}"

        # Width adapts to whichever line is longest
        width = max(len(id_line), len(balance_str)) + 4

        return (
            f"\n"
            f"  ┌{'─' * width}┐\n"
            f"  │  {id_line:<{width - 2}}│\n"
            f"  ├{'─' * width}┤\n"
            f"  │  Balance: {balance_str:<{width - 11}}│\n"
            f"  └{'─' * width}┘\n"
        )
