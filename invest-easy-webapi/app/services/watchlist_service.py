from typing import Annotated
import uuid
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.db import get_async_session
from ..domain.watch_list import WatchList
from sqlalchemy import select
from ..domain.instruments import Instrument


class WatchlistService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ):
        self.session = session

    async def add_to_watchlist(
        self,
        user_id: uuid.UUID,
        code: str,
        tags: str | None = None,
        notes: str | None = None,
    ):
        """
        Add an instrument to user's watchlist

        Args:
            user_id: User ID
            code: Instrument code to add
            tags: Optional tags (comma separated)
            notes: Optional notes

        Returns:
            The created WatchedInstrument record
        """
        instrument_id = await self.session.scalars(
            select(Instrument.id).where(
                Instrument.code == code, Instrument.is_active == True
            )
        )
        instrument_id = instrument_id.one_or_none()
        if not instrument_id:
            raise ValueError(f"No such instrument found: {code}")
        watched = WatchList.add_to_watchlist(user_id, instrument_id, tags, notes)
        self.session.add(watched)
        await self.session.commit()
        return watched

    async def remove_from_watchlist(self, user_id: str, instrument_id: str):
        """
        Remove an instrument from user's watchlist

        Args:
            user_id: User ID
            instrument_id: Instrument ID to remove

        Returns:
            bool: True if removed, False if not found
        """
        watched = await self.session.scalars(
            WatchList.get_watch_list_stmp(user_id, instrument_id)
        )
        watched = watched.one_or_none()

        if watched:
            watched.remove_from_watchlist()
            await self.session.commit()

    async def get_watchlist(self, user_id: uuid.UUID):
        """
        Get user's watchlist

        Args:
            user_id: User ID

        Returns:
            List of watched instruments
        """
        list = await self.session.scalars(
            select(WatchList, Instrument)
            .join(Instrument, Instrument.id == WatchList.instrument_id)
            .where(
                WatchList.user_id == user_id,
                WatchList.is_active == True,
                Instrument.is_active == True,
            )
        )
        return [
            {
                "code": instrument.code,
                "name": instrument.name,
                "notes": watch.notes,
            }
            for watch, instrument in list.all()
        ]

    async def is_watched(self, user_id: str, instrument_id: str):
        """
        Check if instrument is in user's watchlist

        Args:
            user_id: User ID
            instrument_id: Instrument ID to check

        Returns:
            bool: True if watched, False otherwise
        """
        watched = await self.session.scalars(
            WatchList.get_watch_list_stmp(user_id, instrument_id)
        )
        watched = watched.one_or_none()
        return True if watched else False
