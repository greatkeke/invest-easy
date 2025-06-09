import uuid
from enum import Enum
from .base_domain import Base
from sqlalchemy import UUID, Float, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column


class OrderStatus(Enum):
    QUEUED = 1
    WORKING = 2
    FILLED = 3
    DEACTIVATED = 4


class Order(Base):
    __tablename__ = "orders"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    position_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    trade_in: Mapped[Boolean] = mapped_column(Boolean, nullable=False, default=True)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.QUEUED)
