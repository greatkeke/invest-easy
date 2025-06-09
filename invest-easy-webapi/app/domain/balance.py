import uuid
from enum import Enum
from sqlalchemy import (
    UUID,
    String,
    Float,
    Boolean,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column
from .base_domain import Base


class BalanceType(Enum):
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    TRADE_BUY = "trade_buy"
    TRADE_SELL = "trade_sell"


class Balance(Base):
    __tablename__ = "balances"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    balance = mapped_column(Float, nullable=False, default=0.00)
    ccy = mapped_column(String(3), nullable=False, default="HKD")


class BalanceHistory(Base):
    __tablename__ = "balance_histories"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    ccy = mapped_column(String(3), nullable=False)
    type = mapped_column(
        SQLEnum(BalanceType),
        nullable=False,
        default=BalanceType.TRANSFER_IN,
    )
    is_increment = mapped_column(Boolean, nullable=False, default=True)
