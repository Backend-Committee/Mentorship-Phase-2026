""" This Module defines the FileStorage class which handles
the serialization and deserialization of model instances to and from a JSON file."""


import json
import os
from models.BaseModel import BaseModel


class FileStorage:
    """FileStorage class that serializes and deserializes instances to/from a JSON file."""
  
    def __init__(self, **kwargs):
        """Initialize the FileStorage with class mappings."""
        from models.Book import Book
        from models.User import User
        from models.Transaction import Transaction

        self.__objects = {
            "Book": {},
            "User": {},
            "Transaction": {}
        }
        
        self.__classes = {
            "Book": Book,
            "User": User,
            "Transaction": Transaction
        }
        # Set file paths for storage
        self.paths = {
            "Book": "storage/books.json",
            "User": "storage/users.json",
            "Transaction": "storage/transactions.json"
        }
        # Create storage directory if it doesn't exist
        os.makedirs("storage", exist_ok=True)
        self.reload()

    def all(self, cls=None):
        """Return the dictionary of all objects, optionally filtered by class."""
        if cls is None:
            return self.__objects
        cls_name = cls.__name__
        if cls_name in self.__objects:
            return self.__objects[cls_name]
        return {}
    
    def new(self, obj):
        """Add a new object to the storage dictionary."""
        cls_name = type(obj).__name__
        if cls_name in self.__objects:
            key = f"{cls_name}.{obj.id}"
            self.__objects[cls_name][key] = obj
    
    def save(self):
        """Serialize the objects to their respective JSON files."""
        for cls_name, objects in self.__objects.items():
            file_path = self.paths.get(cls_name, f"storage/{cls_name.lower()}.json")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump({key: obj.to_dict() for key, obj in objects.items()}, f, indent=2)


    def reload(self):
        """Deserialize the JSON files to objects."""
        for cls_name, cls in self.__classes.items():
            file_path = self.paths.get(cls_name, f"storage/{cls_name.lower()}.json")
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        obj_dicts = json.load(f)
                        for key, obj_data in obj_dicts.items():
                            obj = cls(**obj_data)
                            self.new(obj)
                except json.JSONDecodeError:
                    # File is empty or corrupted, skip
                    pass
      
