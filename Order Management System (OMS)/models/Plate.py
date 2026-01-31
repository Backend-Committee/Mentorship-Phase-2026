"""Plate model definition."""

from sqlalchemy import Column, Integer, String, DateTime , Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from engin.Base import BASE
import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import Boolean
import uuid

from models.Order import OrderItems



class Plate(BASE):
    __tablename__ = 'plates'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=False, default=lambda: str(uuid.uuid4()))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationship to OrderItems using string to avoid circular import
    order_items: Mapped[list["OrderItems"]] = relationship("OrderItems", back_populates="plate")
    
    category_id: Mapped[str] = mapped_column(String, ForeignKey('categories.id'), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="plates")

    picpathid: Mapped[str] = mapped_column(String(255), nullable=False, default=lambda: str(uuid.uuid4()), unique=True)  # Metadata/Id

    def __repr__(self):
        return f"<Plate(id={self.id}, name={self.name}, price={self.price})>"
    


class Category(BASE):
    __tablename__ = 'categories'
    id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=False, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    plates: Mapped[list["Plate"]] = relationship("Plate", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"
    
