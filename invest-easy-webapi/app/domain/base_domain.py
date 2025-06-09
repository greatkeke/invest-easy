from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, default=func.now(), nullable=False)
    is_active = mapped_column(Boolean, default=True, nullable=False)
