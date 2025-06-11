import logging
from fastapi import Depends
import numpy as np
from contextlib import contextmanager
from typing import Annotated, List, Dict, Any, Generator
from datetime import datetime
import futu as ft
from futu import OpenQuoteContext, RET_OK, SubType
from pandas import DataFrame
from ..config import settings
from ..infrastructure.db import (
    get_stock_basicinfo_cache,
    update_stock_basicinfo_cache,
    engine,
)
from sqlalchemy.ext.asyncio import AsyncSession
from pandas import DataFrame
from .db import get_async_session


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

    async def search_stocks(
        self, query: str, market: str = "HK"
    ) -> List[Dict[str, Any]]:
        """
        Search stocks by name or code from Futu OpenD

        Args:
            query: Stock name or code to search for
            market: Market to search in (default: 'HK')

        Returns:
            List of dicts containing matching stocks

        Raises:
            ValueError: If input parameters are invalid
            RuntimeError: If Futu API call fails
        """
        if not query:
            raise ValueError("query cannot be empty")

        # First try to get from cache
        async with AsyncSession(engine) as session:
            cache = await get_stock_basicinfo_cache(
                session, market=market, stock_type=str(ft.SecurityType.STOCK)
            )

            if cache is not None and cache.data is not None:
                data = DataFrame.from_records(cache.data)
            else:
                # Get from API if no cache
                with self._get_quote_ctx() as quote_ctx:
                    ret, data = quote_ctx.get_stock_basicinfo(
                        market, stock_type=ft.SecurityType.STOCK
                    )
                    if ret != RET_OK:
                        error_msg = f"Futu API error: {data}"
                        logging.error(error_msg)
                        raise RuntimeError(error_msg)

                    # Update cache with new data
                    # Convert DataFrame to dict format expected by cache
                    if isinstance(data, DataFrame):
                        records = data.to_dict(orient="records")
                    else:
                        records = []

                    await update_stock_basicinfo_cache(
                        session,
                        market=market,
                        stock_type=str(ft.SecurityType.STOCK),
                        data=records,
                    )
                    data = data  # Keep original DataFrame for processing

        if not isinstance(data, DataFrame):
            return []

        # Filter stocks by name or code
        query = query.lower()
        filtered = data[
            (data["code"].str.lower().str.contains(query))
            | (data["name"].str.lower().str.contains(query))
        ][:10]

        records = filtered.to_dict("records")
        return [
            {
                str(k): None if (isinstance(v, float) and np.isnan(v)) else v
                for k, v in record.items()
            }
            for record in records
        ]
