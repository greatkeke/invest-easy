import logging
import numpy as np
from contextlib import contextmanager
from typing import List, Dict, Any, Generator
from futu import OpenQuoteContext, RET_OK, SubType
from pandas import DataFrame
from ..config import settings


class FutuApiService:
    def __init__(self):
        self._host = settings.futu_openD_host
        self._port = settings.futu_openD_port

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
            ret_sub, _ = quote_ctx.subscribe([code], [SubType.RT_DATA], is_first_push=True, subscribe_push=True)
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
