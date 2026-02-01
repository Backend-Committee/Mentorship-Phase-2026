from abc import ABC, abstractmethod

from features.auth.model import AuthInfo


class IAuthInfoRepo(ABC):
    @abstractmethod
    def create(self, username: str, email: str, hashed_password: str) -> AuthInfo:
        """Create a new AuthInfo record and return it."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> AuthInfo | None:
        """Fetch an AuthInfo by ID. Returns None if not found."""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> AuthInfo | None:
        """Fetch an AuthInfo by username. Returns None if not found."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> AuthInfo | None:
        """Fetch an AuthInfo by email. Returns None if not found."""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete an AuthInfo by ID. Returns True if deleted, False if not found."""
        pass
