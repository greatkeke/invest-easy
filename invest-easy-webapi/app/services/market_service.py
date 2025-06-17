from typing import Annotated, List
from uuid import UUID
from fastapi import Depends
from ..infrastructure.futu_api_service import FutuApiService
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.db import get_async_session
from sqlalchemy import or_, select
from ..domain.instruments import Instrument
from ..domain.positions import Position
from ..domain.accounts import UserAccount
from ..services.watchlist_service import WatchlistService


class MarketService:
    def __init__(
        self,
        futu_api_svc: Annotated[FutuApiService, Depends(FutuApiService)],
        watch_list_svc: Annotated[WatchlistService, Depends(WatchlistService)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ):
        self.futu_api_svc = futu_api_svc
        self.watch_list_svc = watch_list_svc
        self.session = session

    def get_market_snapshot(self, code_list: List[str]):
        data = self.futu_api_svc.get_market_snapshot(code_list=code_list)
        return data

    def get_rt_data(self, code: str):
        """
        Get real-time tick data for a stock

        Args:
            code: Stock code (e.g. 'HK.00700')

        Returns:
            List of dicts containing real-time tick data
        """
        data = self.futu_api_svc.get_rt_data(code=code)
        return data

    async def search_stocks(self, query: str):
        """
        Search stocks by name or code

        Args:
            query: Stock name or code to search for
            market: Market to search in (default: 'HK')

        Returns:
            List of dicts containing matching stocks
        """

        stmt = (
            select(Instrument)
            .where(
                or_(
                    Instrument.code.ilike(f"%{query}%"),
                    Instrument.name.ilike(f"%{query}%"),
                ),
                Instrument.is_active == True,
            )
            .limit(10)
        )

        result = await self.session.execute(stmt)
        instruments = result.scalars().all()

        return [
            {
                "code": instrument.code,
                "name": instrument.name,
                "type": instrument.stock_type,
                "exchange": instrument.exchange_type,
            }
            for instrument in instruments
        ]

    async def get_user_instruments(
        self,
        user_id: UUID,
    ):
        """
        Get all instruments for a user including positions and watchlist

        Args:
            user_id: User ID to fetch instruments for

        Returns:
            List of dicts containing instrument code and name
        """
        # Get positions' instruments
        instrument_result = await self.session.execute(
            select(Instrument)
            .join(UserAccount, UserAccount.id == Position.user_account_id)
            .join(Position, Instrument.id == Position.instrument_id)
            .where(
                UserAccount.user_id == user_id,
                UserAccount.is_active == True,
                Position.is_active == True,
                Instrument.is_active == True,
            )
        )
        position_instruments = [
            {"code": instrument.code, "name": instrument.name}
            for instrument in instrument_result.scalars().all()
        ]

        # Get watchlist instruments
        watchlist_instruments = [
            {"code": item["code"], "name": item["name"]}
            for item in await self.watch_list_svc.get_watchlist(user_id)
        ]

        # Combine and deduplicate by code
        return list({i["code"]: i for i in position_instruments + watchlist_instruments}.values())
