from abc import ABC, abstractmethod

from features.user.model import User


class IUserRepo(ABC):
    @abstractmethod
    def create_user(self, display_name: str, auth_id: int) -> User:
        """Create a new user and return the created User instance."""
        pass

    @abstractmethod
    def get_user(self, id: int) -> User | None:
        """Fetch a user by their ID. Returns None if not found."""
        pass

    @abstractmethod
    def update_user(self, id: int, data: dict) -> User | None:
        """Update a user's data by ID. Returns the updated User, or None if not found."""
        pass

    @abstractmethod
    def delete_user(self, id: int) -> bool:
        """Delete a user by ID. Returns True if deleted, False if not found."""
        pass

    @abstractmethod
    def get_user_by_auth_id(self, auth_id: int) -> User | None:
        """Get User from auth data"""
        pass
