""" 
    This is the base model class for all models in the project.
    JISON-BASE-MODEL 
"""
from datetime import datetime
import uuid
import json
import os

STORAGE_PATH = "./Storage/storage.json"



class BaseModel:
    """
    The BaseModel class serves as the foundational class for all models in the project.
    """
    # class atributes
    global STORAGE_PATH
    storage_path = STORAGE_PATH
    objects = {}

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
            
        self.__new()

  
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

    def __new(self):
        """
        Updates the updated_at attribute with the current datetime.
        """
        self.updated_at = datetime.now()
        # ad the object to the objects dictionary
        cls = type(self)
        if cls not in cls.objects:
            cls.objects[cls] = []
        cls.objects[cls].append(self)


    @classmethod
    def save(cls):
        """
        Saves the current instance to the storage file.
        """
        for class_type, instances in cls.objects.items():
            data = [instance.to_dict() for instance in instances]
            file_path = os.path.join(cls.storage_path)
            with open(file_path, 'w') as f:
                json.dump(data, f)

    @classmethod
    def load(cls):
        """
        Loads all instances from the storage file into the objects dictionary.
        """
        file_path = os.path.join(cls.storage_path)
        if not os.path.exists(file_path):
            return
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            for item in data:
                cls(**item)


    @classmethod
    def all(cls,class_type=None):
        """
        Returns all instances of the class from the objects dictionary.
        """
        if class_type:
            return cls.objects.get(class_type, [])
        return cls.objects
    
    def delete(self):
        """
        Deletes the current instance from the objects dictionary.
        """
        cls = type(self)
        if cls in cls.objects and self in cls.objects[cls]:
            cls.objects[cls].remove(self)
    
    @classmethod
    def clear_storage(cls):
        """
        Clears all instances from the storage file and the objects dictionary.
        """
        cls.objects = {}
        file_path = os.path.join(cls.storage_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    @classmethod
    def del_by_id(cls, id):
        """
        Deletes an instance by its ID from the objects dictionary.
        """
        for class_type, instances in cls.objects.items():
            for instance in instances:
                if instance.id == id:
                    instances.remove(instance)
                    return True
        return False

    