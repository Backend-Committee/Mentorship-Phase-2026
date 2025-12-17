from base_model import BaseModel

class User(BaseModel):
    __slots__ = ("id", "full_name", "borrowed_books")
    serializable_fields = __slots__