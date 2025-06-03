from sqlalchemy import String, Boolean, DateTime, func, text
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column(String, nullable=False)
    ccy = mapped_column(String(3), nullable=False, default=text("HKD"))
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    is_active = mapped_column(Boolean, default=True, nullable=False)


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)
    account_id = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    is_active = mapped_column(Boolean, default=True, nullable=False)
