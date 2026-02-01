from dataclasses import dataclass


@dataclass
class User:
    """Represents the User table — stores the user profile, linked to AuthInfo."""

    id: int
    display_name: str
    auth_id: int  # F.K

    @classmethod
    def from_row(cls, row) -> "User":
        """Hydrate a User instance from a sqlite3.Row object."""
        return cls(
            id=row["id"],
            display_name=row["display_name"],
            auth_id=row["auth_id"],
        )
