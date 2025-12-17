from base_model import BaseModel

class Book(BaseModel):
    # the id is ISBN or an integer if ISBN is not provided 
    __slots__ = ("id", "title", "author", "copies")
    serializable_fields = __slots__