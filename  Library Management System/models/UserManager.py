""" This module defines the UserManager class for managing users in the library system."""

from models.User import User


class UserManager:
    """UserManager class that manages all user operations."""

    def __init__(self, storage):
        """Initialize UserManager with a storage engine."""
        self.storage = storage

    def add_user(self, name, email, membership_date):
        """Add a new user to the library."""
        user = User(
            name=name,
            email=email,
            membership_date=membership_date,
            active=True
        )
        self.storage.new(user)
        self.storage.save()
        return user

    def get_all_users(self):
        """Return all users in the library."""
        return self.storage.all(User)

    def get_user_by_id(self, user_id):
        """Get a specific user by their ID."""
        users = self.get_all_users()
        key = f"User.{user_id}"
        return users.get(key)

    def get_active_users(self):
        """Return only active users."""
        users = self.get_all_users()
        return {key: user for key, user in users.items() if user.active}

    def deactivate_user(self, user_id):
        """Deactivate a user account."""
        user = self.get_user_by_id(user_id)
        if user:
            user.active = False
            user.updated_at = __import__('datetime').datetime.now()
            self.storage.save()
            return user
        return None

    def activate_user(self, user_id):
        """Activate a user account."""
        user = self.get_user_by_id(user_id)
        if user:
            user.active = True
            user.updated_at = __import__('datetime').datetime.now()
            self.storage.save()
            return user
        return None

    def delete_user(self, user_id):
        """Delete a user from the library."""
        users = self.get_all_users()
        key = f"User.{user_id}"
        if key in users:
            del users[key]
            self.storage.save()
            return True
        return False
