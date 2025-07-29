from datetime import datetime, timedelta
import logging
from fastapi import Depends
import numpy as np
from contextlib import contextmanager
from typing import Annotated, List, Dict, Any, Generator
import futu as ft
from futu import OpenQuoteContext, RET_OK, SubType
from pandas import DataFrame
from ..config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from pandas import DataFrame
from .db import get_async_session
from ..domain.instruments import Instrument
from sqlalchemy import func, select


class FutuApiService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self._host = settings.futu_openD_host
        self._port = settings.futu_openD_port
        self.session = session

    @contextmanager
    def _get_quote_ctx(self) -> Generator[OpenQuoteContext, None, None]:
        """Context manager for quote connection"""
        quote_ctx = OpenQuoteContext(host=self._host, port=self._port)
        try:
            yield quote_ctx
        finally:
            quote_ctx.close()

    def get_market_snapshot(
        self,
        code_list: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Get market snapshot data from Futu OpenD

        Args:
            code_list: List of stock codes (e.g. ['HK.00700'])

        Returns:
            List of dicts containing market snapshot data

        Raises:
            ValueError: If input parameters are invalid
            RuntimeError: If Futu API call fails
        """
        if not code_list:
            raise ValueError("code_list cannot be empty")

        with self._get_quote_ctx() as quote_ctx:
            ret, data = quote_ctx.get_market_snapshot(code_list)
            if ret != RET_OK:
                error_msg = f"Futu API error: {data}"
                logging.error(error_msg)
                raise RuntimeError(error_msg)

            if isinstance(data, DataFrame):
                records = data.to_dict("records")
                return [
                    {
                        str(k): None if (isinstance(v, float) and np.isnan(v)) else v
                        for k, v in record.items()
                    }
                    for record in records
                ]
            return []

    def get_rt_data(
        self,
        code: str,
    ) -> List[Dict[str, Any]]:
        """
        Get real-time tick data from Futu OpenD

        Args:
            code: Stock code (e.g. 'HK.00700')

        Returns:
            List of dicts containing real-time tick data

        Raises:
            ValueError: If input parameters are invalid
            RuntimeError: If Futu API call fails
        """
        if not code:
            raise ValueError("code cannot be empty")

        with self._get_quote_ctx() as quote_ctx:
            # First subscribe to the stock data
            ret_sub, _ = quote_ctx.subscribe(
                [code], [SubType.RT_DATA], is_first_push=True, subscribe_push=True
            )
            if ret_sub != RET_OK:
                error_msg = f"Failed to subscribe to {code}"
                logging.error(error_msg)
                raise RuntimeError(error_msg)

            # Then get the real-time data (only code parameter is required)
            ret, data = quote_ctx.get_rt_data(code)
            if ret != RET_OK:
                error_msg = f"Futu API error: {data}"
                logging.error(error_msg)
                raise RuntimeError(error_msg)

            # Unsubscribe after getting data
            quote_ctx.unsubscribe([code], [SubType.RT_DATA])

            if isinstance(data, DataFrame):
                records = data.to_dict("records")
                return [
                    {
                        str(k): None if (isinstance(v, float) and np.isnan(v)) else v
                        for k, v in record.items()
                    }
                    for record in records
                ]
            return []

    async def initialize_all_markets_instruments(self) -> int:
        """
        Initialize all markets instruments by generating Cartesian product of markets and types,
        then calling initialize_a_market_instruments for each combination.

        Returns:
            Total number of instruments initialized across all markets/types

        Raises:
            RuntimeError: If Futu API call fails
        """
        # Check last update time
        latest_update = (
            await self.session.execute(select(func.max(Instrument.updated_at)))
        ).scalar_one_or_none()

        if latest_update is None:
            logging.info("No instruments found in database")
        else:
            # Ensure latest_update is a datetime object
            latest_update_dt = (
                latest_update
                if isinstance(latest_update, datetime)
                else latest_update.to_datetime()
            )
            if (datetime.now() - latest_update_dt) < timedelta(days=7):
                logging.info("Instruments are up-to-date")
                return 0

        market_list = [ft.Market.HK, ft.Market.US, ft.Market.SH, ft.Market.SZ]
        type_list = [
            ft.SecurityType.STOCK,
            ft.SecurityType.ETF,
            ft.SecurityType.IDX,
        ]

        total_count = 0
        for market in market_list:
            for security_type in type_list:
                try:
                    logging.info(
                        f"Start to initialze instruments of {market} with {security_type}."
                    )
                    count = await self.initialize_a_market_instruments(
                        market, security_type
                    )
                    logging.info(f"{count} instruments have been upserted.")
                    total_count += count
                except Exception as e:
                    logging.error(
                        f"Failed to initialize {market} {security_type}: {str(e)}"
                    )
                    continue

        return total_count

    async def initialize_a_market_instruments(self, market: str, type: str) -> int:
        """
        Initialize instruments for a market and store them in database.
        Only inserts new instruments or updates existing ones if they have changed.

        Args:
            market: Market identifier (e.g. 'HK', 'US')
            type: Security type (e.g. 'STOCK', 'ETF')

        Returns:
            Number of instruments inserted or updated

        Raises:
            RuntimeError: If Futu API call fails
        """
        with self._get_quote_ctx() as quote_ctx:
            ret, data = quote_ctx.get_stock_basicinfo(market, stock_type=type)
            if ret != RET_OK:
                error_msg = f"Futu API error: {data}"
                logging.error(error_msg)
                raise RuntimeError(error_msg)

            if not isinstance(data, DataFrame):
                return 0

            # Get existing instruments from database
            existing_instruments = await self.session.execute(
                select(Instrument).where(Instrument.code.in_(data["code"].tolist()))
            )
            existing_instruments = {i.code: i for i in existing_instruments.scalars()}

            # Process API data
            update_count = 0
            insert_count = 0
            record = None  # Initialize record variable
            for record in data.to_dict("records"):
                code = record.get("code")
                existing = existing_instruments.get(code)

                if existing:
                    existing.upsert(record)
                    update_count += 1
                else:
                    existing = Instrument()
                    existing.market = market
                    existing.upsert(record)
                    self.session.add(existing)
                    insert_count += 1

            try:
                await self.session.commit()
                logging.info(
                    f"Inserted {insert_count} new instruments, updated {update_count} existing instruments"
                )
            except Exception as e:
                await self.session.rollback()
                if record:
                    record_details = "\n".join([f"{k}: {v}" for k, v in record.items()])
                    logging.error(
                        f"Failed to upsert record (code: {record.get('code', 'N/A')})\nException: str({e}) \nDetail:\n{record_details}"
                    )
                else:
                    logging.error("Failed to upsert record: No record data available")
                raise e
            finally:
                return insert_count + update_count
