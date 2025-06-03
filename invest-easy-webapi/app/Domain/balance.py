from typing import List
import uuid
from sqlalchemy import (
    UUID,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Balance(Base):
    __tablename__ = "balances"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    balance = mapped_column(Float, nullable=False, default=0.00)
    ccy = mapped_column(String(3), nullable=False, default="HKD")
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, default=func.now(), nullable=False)


class BalanceHistory(Base):
    __tablename__ = "balance_histories"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    ccy = mapped_column(String(3), nullable=False)
    transfer_in = mapped_column(Boolean, default=True, nullable=False)
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
