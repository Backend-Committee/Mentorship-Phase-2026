import sqlite3

from features.auth.IAuthInfoRepo import IAuthInfoRepo
from features.auth.model import AuthInfo


class AuthInfoRepo(IAuthInfoRepo):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create(self, username: str, email: str, hashed_password: str) -> AuthInfo:
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO AuthInfo (username, email, hashed_password) VALUES (?, ?, ?)",
                (username, email, hashed_password),
            )
            return AuthInfo(
                id=cursor.lastrowid,
                username=username,
                email=email,
                hashed_password=hashed_password,
            )

    def get_by_id(self, id: int) -> AuthInfo | None:
        cursor = self.conn.execute("SELECT * FROM AuthInfo WHERE id = ?", (id,))
        row = cursor.fetchone()
        return AuthInfo.from_row(row) if row else None

    def get_by_username(self, username: str) -> AuthInfo | None:
        cursor = self.conn.execute(
            "SELECT * FROM AuthInfo WHERE username = ?", (username,)
        )
        row = cursor.fetchone()
        return AuthInfo.from_row(row) if row else None

    def get_by_email(self, email: str) -> AuthInfo | None:
        cursor = self.conn.execute("SELECT * FROM AuthInfo WHERE email = ?", (email,))
        row = cursor.fetchone()
        return AuthInfo.from_row(row) if row else None

    def delete(self, id: int) -> bool:
        with self.conn:
            cursor = self.conn.execute("DELETE FROM AuthInfo WHERE id = ?", (id,))
            return cursor.rowcount > 0
