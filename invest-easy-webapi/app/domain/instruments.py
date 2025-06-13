import uuid
from .base_domain import Base
from sqlalchemy import UUID, String, Integer, Boolean, Float, DateTime
from sqlalchemy.orm import mapped_column
from datetime import datetime


class Instrument(Base):
    __tablename__ = "instruments"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = mapped_column(String, nullable=False)
    name = mapped_column(String, nullable=False)
    lot_size = mapped_column(Integer)
    stock_type = mapped_column(String, nullable=True, default='None')  # Stores SecurityType value
    stock_child_type = mapped_column(String)  # Stores WrtType value, nullable
    stock_owner = mapped_column(String)  # Nullable
    option_type = mapped_column(String)  # Stores OptionType value, nullable
    strike_time = mapped_column(DateTime)  # Nullable
    strike_price = mapped_column(Float)  # Nullable
    suspension = mapped_column(Boolean, default=False)
    listing_date = mapped_column(DateTime, nullable=True)
    stock_id = mapped_column(Integer)
    delisting = mapped_column(Boolean, default=False)
    index_option_type = mapped_column(String)  # Nullable
    main_contract = mapped_column(Boolean, default=False)
    last_trade_time = mapped_column(DateTime)  # Nullable
    exchange_type = mapped_column(String, nullable=True, default='None')  # Stores ExchType value

    def _format_value(self, field, value):
        datetime_fields = {"strike_time", "listing_date", "last_trade_time"}
        if value == "N/A":
            value = None
        elif field in datetime_fields and isinstance(value, str):
            value = (
                datetime.strptime(value, "%Y-%m-%d")
                if value != "N/A" and value != ""
                else None
            )
        return value

    def upsert(self, record: dict):
        for field, value in record.items():
            value = self._format_value(field, value)
            if hasattr(self, field) and getattr(self, field) != value:
                setattr(self, field, value)
