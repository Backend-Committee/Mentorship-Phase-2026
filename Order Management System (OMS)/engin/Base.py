from sqlalchemy.orm import DeclarativeBase


class BASE(DeclarativeBase):
    """Base class for all ORM models."""
    __abstract__ = True
    pass