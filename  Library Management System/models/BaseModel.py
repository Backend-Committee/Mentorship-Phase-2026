""" This module defines the BaseModel 
class which serves as a base for all models 
in the application. ((interface)) 
"""


import uuid
from datetime import datetime

class BaseModel:
    """BaseModel class that defines all common"""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance."""
        # start with a new initialization in case no kwargs are provided
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        if not kwargs:
            pass # new instance in the database
            return
        
        # When loading from storage, override the default values
        for key, value in kwargs.items():
            if key == "created_at" or key == "updated_at":
                setattr(self, key, datetime.fromisoformat(value))
            elif key != "__class__":
                setattr(self, key, value)

        # Ensure all basic attributes are set when loading from storage
        for attr in ["id", "created_at", "updated_at"]:
            if not hasattr(self, attr):
                raise ValueError(f"Missing required attribute: {attr}")

  
    def __str__(self):
        """
        this is the method return string representation of the BaseModel instance
        """
        obj_dict = (self.__dict__).copy()
        return '[{}] ({}) {}'.format(type(self).__name__, self.id, obj_dict)


    def to_dict(self):
        """
        this function it has no argumants and returns
        a dictionary containing all keys/values of __dict__ of the instance
        """
        obj_dict = {}
        for key, value in self.__dict__.items():
            if key not in ['created_at', 'updated_at']:
                obj_dict[key] = value
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
