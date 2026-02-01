from dataclasses import dataclass


@dataclass
class AuthInfo:
    """Represents the AuthInfo table — stores user credentials."""

    id: int
    username: str
    email: str
    hashed_password: str

    @classmethod
    def from_row(cls, row) -> "AuthInfo":
        """Hydrate an AuthInfo instance from a sqlite3.Row object."""
        return cls(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            hashed_password=row["hashed_password"],
        )
