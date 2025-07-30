from typing import Annotated, List
from uuid import UUID
from fastapi import Depends
from ..infrastructure.futu_api_service import FutuApiService
from ..infrastructure.akshare_service import AkshareService
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.db import get_async_session
from sqlalchemy import or_, select
from ..domain.instruments import Instrument
from ..domain.positions import Position
from ..domain.accounts import UserAccount
from ..domain.snapshots import Snapshots
from ..services.watchlist_service import WatchlistService
import logging


class MarketService:
    def __init__(
        self,
        futu_api_svc: Annotated[FutuApiService, Depends(FutuApiService)],
        akshare_svc: Annotated[AkshareService, Depends(AkshareService)],
        watch_list_svc: Annotated[WatchlistService, Depends(WatchlistService)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ):
        self.futu_api_svc = futu_api_svc
        self.akshare_svc = akshare_svc
        self.watch_list_svc = watch_list_svc
        self.session = session

    async def get_market_snapshot(self, code_list: List[str]) -> List[dict]:
        """
        Get market snapshot data for a list of stock codes.
        - For US codes (starting with 'US.'): Retrieve from database snapshots table
        - For non-US codes: Retrieve from Futu API
        - Merge both datasets and return combined results

        Args:
            code_list: List of stock codes (e.g. ['US.AAPL', 'HK.00700'])

        Returns:
            List of dicts containing market snapshot data

        Raises:
            ValueError: If input parameters are invalid
            RuntimeError: If API calls fail
        """
        if not code_list:
            return []

        # Filter US and non-US codes
        us_codes = [code for code in code_list if code.startswith("US.")]
        non_us_codes = [code for code in code_list if not code.startswith("US.")]

        all_snapshots = []

        # Retrieve snapshots from database for US codes
        if us_codes:
            us_snapshots = await self._get_us_snapshots_from_db(us_codes)
            all_snapshots.extend(us_snapshots)

        # Retrieve snapshots from Futu API for non-US codes
        if non_us_codes:
            try:
                non_us_snapshots = self.futu_api_svc.get_market_snapshot(
                    code_list=non_us_codes
                )
                all_snapshots.extend(non_us_snapshots)
            except Exception as e:
                # Log error but continue with available data
                import logging

                logging.error(f"Failed to get non-US snapshots from Futu API: {str(e)}")
                # Return what we have so far
                pass

        return all_snapshots

    async def _get_us_snapshots_from_db(self, us_codes: List[str]) -> List[dict]:
        """
        Retrieve US stock snapshots from the database snapshots table.

        Args:
            us_codes: List of US stock codes (e.g. ['US.AAPL', 'US.GOOG'])

        Returns:
            List of dicts containing market snapshot data
        """
        try:
            # Query snapshots from database
            stmt = (
                select(Snapshots,Instrument.name)
                .join(Instrument, Instrument.id == Snapshots.instrument_id)
                .where(
                    Snapshots.futu_code.in_(us_codes),
                    Snapshots.is_active == True,
                    Instrument.is_active == True,
                )
            )
            result = await self.session.execute(stmt)
            db_snapshots = result.all()

            # Convert database snapshots to the expected format
            snapshots_data = []
            for record in db_snapshots:
                snapshot = record[0]
                name = record[1]
                snapshot_data = {
                    "code": snapshot.futu_code,
                    "name": name,
                    "last_price": snapshot.latest_price,
                    "change_rate": snapshot.change_percent,
                    "change_value": snapshot.change_amount,
                    "open_price": snapshot.open_price,
                    "high_price": snapshot.high_price,
                    "low_price": snapshot.low_price,
                    "prev_close_price": snapshot.previous_close,
                    "volume": snapshot.volume,
                    "turnover": snapshot.turnover,
                    "market_cap": snapshot.market_cap,
                    "pe_ratio": snapshot.pe_ratio,
                    "amplitude": snapshot.amplitude,
                    "turnover_rate": snapshot.turnover_rate,
                    # Add timestamp or other fields as needed
                }
                # Remove None values
                snapshot_data = {
                    k: v for k, v in snapshot_data.items() if v is not None
                }
                snapshots_data.append(snapshot_data)

            return snapshots_data
        except Exception as e:
            import logging

            logging.error(f"Failed to get US snapshots from database: {str(e)}")
            return []

    async def get_rt_data(self, code: str):
        """
        Get real-time tick data for a stock

        Args:
            code: Stock code (e.g. 'HK.00700')

        Returns:
            List of dicts containing real-time tick data
        """
        if code.startswith("US."):
            # For US stocks, query snapshots table to get the symbol and call akshare
            try:
                # Query snapshots from database to get the raw symbol code
                stmt = (
                    select(Snapshots)
                    .where(
                        Snapshots.futu_code == code,
                        Snapshots.is_active == True,
                    )
                    .limit(1)
                )
                result = await self.session.execute(stmt)
                snapshot = result.scalar_one_or_none()
                
                if snapshot and snapshot.code:
                    # Call akshare service with the raw symbol code
                    data = self.akshare_svc.get_rtdata(symbol=snapshot.code)
                    return data
                else:
                   return []
            except Exception as e:
                logging.error(f"Failed to get US real-time data from akshare for {code}: {str(e)}")
                # Fallback to Futu API on error
                return []
        else:
            # For non-US stocks, use existing Futu API logic
            return self.futu_api_svc.get_rt_data(code=code)

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
        return list(
            {
                i["code"]: i for i in position_instruments + watchlist_instruments
            }.values()
        )
