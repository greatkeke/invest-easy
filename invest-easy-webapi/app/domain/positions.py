import uuid
from .base_domain import Base
from sqlalchemy import UUID, Float
from sqlalchemy.orm import Mapped, mapped_column


class Position(Base):
    __tablename__ = "positions"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    avg_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    percentage: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
