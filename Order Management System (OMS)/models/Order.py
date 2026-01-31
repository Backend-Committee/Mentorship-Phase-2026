"""Order model definition."""
from sqlalchemy import Column, Integer, String, DateTime 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from engin.Base import BASE
import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import Boolean
import uuid

# from models.Plate import Plate # Removed to avoid circular import

class Order(BASE):
        __tablename__ = 'orders'
        id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=False, default=lambda: str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
        user: Mapped["user"] = relationship("user", back_populates="orders")
        items : Mapped[list['OrderItems']] = relationship(back_populates="order")
        payment_status: Mapped[bool] = mapped_column(Boolean, default=False)
        payment_method: Mapped[str] = mapped_column(String, nullable=True) # e.g., 'credit_card', 'cash'
        on_place: Mapped[bool] = mapped_column(Boolean, default=False)
        delivered: Mapped[bool] = mapped_column(Boolean, default=False)
        created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
        updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)



class OrderItems(BASE):
    __tablename__ = 'order_items'
    # from models.Plate import Plate # Avoid circular import inside class if possible, prefer string reference
    
    id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=False, default=lambda: str(uuid.uuid4()))
    order_id: Mapped[str] = mapped_column(String, ForeignKey('orders.id'))
    plate_id: Mapped[str] = mapped_column(String, ForeignKey('plates.id'))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    order: Mapped["Order"] = relationship(back_populates="items")
    plate: Mapped["Plate"] = relationship("Plate", back_populates="order_items")
