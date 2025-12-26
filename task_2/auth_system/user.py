class User:
    __slots__ = (
        "username",
        "email",
        "password",
    )

    def __init__(self, username: str, email: str, password: str | None):
        self.username = username
        self.email = email
        self.password = password
    
    @classmethod
    def from_dict(cls, dict):
        return cls(dict['username'], dict['email'], None)
    
    def __repr__(self):
        return self.username
        
    def __str__(self):
        return self.username