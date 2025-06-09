import uuid
from .base_domain import Base
from sqlalchemy import UUID, String
from sqlalchemy.orm import mapped_column


class Instrument(Base):
    __tablename__ = "instruments"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column(String, nullable=False)
    code = mapped_column(String(16), nullable=False)
