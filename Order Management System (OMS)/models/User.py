"""User model definition."""
from sqlalchemy import Column, Integer, String, DateTime 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from engin.Base import BASE
import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import Boolean
import uuid

from models.Order import Order


class user(BASE):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=False, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="counter") # super_admin, admin, counter
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")


    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"