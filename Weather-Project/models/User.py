""" This is the User model class for the project.
    JISON-USER-MODEL
"""


from models.Base_model import BaseModel
from bcrypt import hashpw, gensalt, checkpw

class User(BaseModel):
    """
    The User class represents a user in the system.
    Inherits from BaseModel.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new User instance."""
        super().__init__(*args, **kwargs)
        self.username = kwargs.get('username', "")
        self.email = kwargs.get('email', "")
        password = kwargs.get('password', None)
        
        # If password is already hashed (from storage), use it directly
        if password and password.startswith('$2'):
            self.__password = password
        elif password:
            self.__password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        else:
            self.__password = None

    def set_password(self, password):
        """Set the user's password."""
        if not password:
            raise ValueError("Password cannot be empty.")

        self.__password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the stored password."""
        if self.__password is None:
            return False
        return checkpw(password.encode('utf-8'), self.__password.encode('utf-8'))
    
    def to_dict(self):
        """Convert User instance to dictionary, including password for storage."""
        user_dict = super().to_dict()
        # Include the hashed password for storage
        user_dict['password'] = self.__password
        return user_dict

    def __str__(self):
        """Return string representation of the User instance."""
        obj_dict = (self.__dict__).copy()
        if '_User__password' in obj_dict:
            del obj_dict['_User__password']
        return '[{}] ({}) {}'.format(type(self).__name__, self.id, obj_dict)



    @classmethod
    def get_user_by_username(cls, username):
        """Return user object by username from cls.objects"""
        # Load users from storage
        cls.load()
        
        # Check if User class is in objects
        if cls not in cls.objects:
            return None
        
        # Search through all users
        for user in cls.objects[cls]:
            if user.username == username:
                return user
        return None