from datetime import datetime, date
from sqlalchemy import (
    String, Integer, Float, Date, DateTime, Boolean,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Plan(Base):
    __tablename__ = "plans"

    plan_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    members = relationship("Member", back_populates="plan")

    def __repr__(self) -> str:
        return f"<Plan id={self.plan_id} name={self.plan_name} price={self.price}>"


class Member(Base):
    __tablename__ = "members"
    __table_args__ = (
        UniqueConstraint("email", name="uq_members_email"),
        UniqueConstraint("phone", name="uq_members_phone"),
    )

    member_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)

    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)

    join_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.plan_id"), nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    plan = relationship("Plan", back_populates="members")
    payments = relationship("Payment", back_populates="member", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Member id={self.member_id} name={self.first_name} {self.last_name}>"


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.member_id"), nullable=False)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    paid_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    method: Mapped[str] = mapped_column(String(40), nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    member = relationship("Member", back_populates="payments")

    def __repr__(self) -> str:
        return f"<Payment id={self.payment_id} member_id={self.member_id} amount={self.amount}>"
