import uuid
from .base_domain import Base
from sqlalchemy import UUID, String, Integer, Float, DateTime
from sqlalchemy.orm import mapped_column
from datetime import datetime


class Snapshots(Base):
    __tablename__ = "snapshots"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instrument_id = mapped_column(UUID(as_uuid=True), nullable=False)
    market = mapped_column(String, nullable=False)
    code = mapped_column(String, nullable=False, index=True)  # Code for historical data
    futu_code = mapped_column(String, nullable=False)
    name_cn = mapped_column(String, nullable=False, index=True)
    latest_price = mapped_column(Float)  # Unit: USD
    change_amount = mapped_column(Float)  # Unit: USD
    change_percent = mapped_column(Float)  # Unit: %
    open_price = mapped_column(Float)  # Unit: USD
    high_price = mapped_column(Float)  # Unit: USD
    low_price = mapped_column(Float)  # Unit: USD
    previous_close = mapped_column(Float)  # Unit: USD
    market_cap = mapped_column(Float)  # Unit: USD
    pe_ratio = mapped_column(Float)
    volume = mapped_column(Float)
    turnover = mapped_column(Float)  # Unit: USD
    amplitude = mapped_column(Float)  # Unit: %
    turnover_rate = mapped_column(Float)  # Unit: %
    updated_at = mapped_column(DateTime, default=datetime.now(), index=True)

    def _format_value(self, field, value):
        if value == "N/A":
            value = None
        if value == "NaN":
            value = None
        return value

    def upsert(self, record: dict):
        any_changed = False
        for field, value in record.items():
            value = self._format_value(field, value)
            if hasattr(self, field) and getattr(self, field) != value:
                setattr(self, field, value)
                any_changed = True
        if any_changed:
            self.updated_at = datetime.now()
