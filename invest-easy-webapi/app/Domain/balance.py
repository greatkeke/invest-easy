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
    user_account_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_accounts.id"), nullable=False
    )
    balance = mapped_column(Float, nullable=False, default=0.00)
    ccy = mapped_column(String(3), nullable=False, default="HKD")
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    user_account = relationship("UserAccount", back_populates="balances")
    balance_histories: Mapped[List["BalanceHistory"]] = relationship(
        "BalanceHistory", back_populates="balance"
    )


class BalanceHistory(Base):
    __tablename__ = "balance_histories"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("balances.id"), nullable=False
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    ccy = mapped_column(String(3), nullable=False)
    transfer_in = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    balance = relationship("Balance", back_populates="balance_histories")
