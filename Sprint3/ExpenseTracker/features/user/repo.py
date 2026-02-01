import sqlite3

from features.user.IUserRepo import IUserRepo
from features.user.model import User


class UserRepo(IUserRepo):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_user(self, display_name: str, auth_id: int) -> User:
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO User (display_name, auth_id) VALUES (?, ?)",
                (display_name, auth_id),
            )
            return User(id=cursor.lastrowid, display_name=display_name, auth_id=auth_id)

    def get_user(self, id: int) -> User | None:
        cursor = self.conn.execute("SELECT * FROM User WHERE id = ?", (id,))
        row = cursor.fetchone()
        return User.from_row(row) if row else None

    def update_user(self, id: int, data: dict) -> User | None:
        # Build SET clause dynamically from provided data
        # Only allow known User columns to prevent injection
        allowed = {"display_name"}
        filtered = {k: v for k, v in data.items() if k in allowed}

        if not filtered:
            return self.get_user(id)

        set_clause = ", ".join(f"{k} = ?" for k in filtered)
        values = list(filtered.values()) + [id]

        with self.conn:
            self.conn.execute(f"UPDATE User SET {set_clause} WHERE id = ?", values)
        return self.get_user(id)

    def delete_user(self, id: int) -> bool:
        with self.conn:
            cursor = self.conn.execute("DELETE FROM User WHERE id = ?", (id,))
            return cursor.rowcount > 0

    def get_user_by_auth_id(self, auth_id: int) -> User | None:
        cursor = self.conn.execute("SELECT * FROM User WHERE auth_id = ?", (auth_id,))
        row = cursor.fetchone()
        return User.from_row(row) if row else None
