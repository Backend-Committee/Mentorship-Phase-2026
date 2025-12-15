""" This module defines the User class representing a user in the library management system."""

from models.BaseModel import BaseModel
class User(BaseModel):
    """User class that represents a user in the library management system."""

    def __init__(self, *args, **kwargs):
        """Initialize a new User instance."""
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name', "")
        self.email = kwargs.get('email', "")
        self.membership_date = kwargs.get('membership_date', "")
        self.active = kwargs.get('active', True)