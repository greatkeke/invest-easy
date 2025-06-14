import uuid
from datetime import datetime
from .base_domain import Base
from sqlalchemy import UUID, String, DateTime, ForeignKey, select
from sqlalchemy.orm import mapped_column, relationship


class WatchList(Base):
    __tablename__ = "watch_list"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    instrument_id = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tags = mapped_column(String, nullable=True)  # Comma separated tags
    notes = mapped_column(String, nullable=True)  # User notes

    @classmethod
    def add_to_watchlist(cls, user_id, instrument_id, tags=None, notes=None):
        """Add an instrument to user's watchlist"""
        watched = cls(
            user_id=user_id, instrument_id=instrument_id, tags=tags, notes=notes
        )
        return watched

    def remove_from_watchlist(self):
        """Remove an instrument from user's watchlist"""
        self.is_active = False
        self.updated_at = datetime.now()

    @classmethod
    def get_watch_list_stmp(cls, user_id, instrument_id=None):
        stmp = select(WatchList).where(
            WatchList.user_id == user_id,
            WatchList.is_active == True,
        )
        if instrument_id != None:
            stmp.where(
                WatchList.instrument_id == instrument_id,
            )
        return stmp
