class BaseModel:    
    serializable_fields = ()
    
    def __init__(self, **kwargs):        
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise FieldDoesntExistError(
                    f"field {key} doesn't exist in entity {self}, so it can't be updated"
                )

    def serialize(self):
        return dict(getattr(self, field) for field in self.serializable_fields)

    def __str__(self):
        if hasattr(self, "id"):
            return f"{self.__class__.__name__} {self.id}"

        return f"{self.__class__.__name__}"


class FieldDoesntExistError(Exception):
    def __init__(self, *args, message):
        self.message = message
        super().__init__(*args)
