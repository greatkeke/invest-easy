from datetime import datetime, timedelta
import logging
from fastapi import Depends
import numpy as np
from contextlib import contextmanager
from typing import Annotated, List, Dict, Any, Generator
import akshare as ak
from pandas import DataFrame
from ..config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from .db import get_async_session
from ..domain.snapshots import Snapshots
from ..domain.instruments import Instrument


class AkshareService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self.session = session
        self.market = "US"

    def _parse_code(self, code: str) -> str:
        """
        Parse code from format like "105.DBGI" to "DBGI" and combine with market.

        Args:
            code: Raw code from AkShare API

        Returns:
            Parsed code in format "market.parsed_code" (e.g., "US.DBGI")
        """
        if not code:
            return code

        # Split by dot and take the part after the last dot
        if "." in code:
            parsed_code = code.split(".")[-1]
        else:
            parsed_code = code

        return f"{self.market}.{parsed_code}"

    def get_us_stock_spot(self) -> List[Dict[str, Any]]:
        """
        Get US stock spot data from AkShare

        Returns:
            List of dicts containing US stock spot data

        Raises:
            RuntimeError: If AkShare API call fails
        """
        try:
            # Get US stock spot data
            stock_us_spot_em_df = ak.stock_us_spot_em()

            if isinstance(stock_us_spot_em_df, DataFrame):
                records = stock_us_spot_em_df.to_dict("records")
                return [
                    {
                        str(k): None if (isinstance(v, float) and np.isnan(v)) else v
                        for k, v in record.items()
                    }
                    for record in records
                ]
            return []
        except Exception as e:
            error_msg = f"AkShare API error: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    async def initialize_snapshots_table(self) -> int:
        """
        Initialize snapshots table with US stock spot data.
        Only initialize if the latest update_at is older than 1 day.
        For existing items, update changed fields; for new items, insert them.

        Returns:
            Number of snapshots inserted or updated

        Raises:
            RuntimeError: If AkShare API call fails or database operation fails
        """
        # Check last update time
        latest_update = (
            await self.session.execute(select(func.max(Snapshots.updated_at)))
        ).scalar_one_or_none()

        if latest_update is not None:
            # Ensure latest_update is a datetime object
            latest_update_dt = (
                latest_update
                if isinstance(latest_update, datetime)
                else datetime.fromisoformat(latest_update.isoformat())
            )
            if (datetime.now() - latest_update_dt) < timedelta(days=1):
                logging.info("InstrumentAK table is up-to-date (less than 1 day old)")
                return 0

        # Get data from AkShare
        try:
            records = self.get_us_stock_spot()
        except Exception as e:
            logging.error(f"Failed to get US stock spot data: {str(e)}")
            return 0

        if not records:
            logging.warning("No US stock spot data received from AkShare")
            return 0

        # Parse all codes upfront to avoid multiple calls to _parse_code
        for record in records:
            raw_code = record.get("代码")
            if raw_code:
                record["parsed_code"] = self._parse_code(raw_code)

        # Get parsed codes for database queries
        parsed_codes = [
            record["parsed_code"] for record in records if record.get("parsed_code")
        ]

        # Get existing instruments from database, get instrument_id from table instruments via parsed_code and instrument.code
        # If no related instrument then ignore this record.
        existing_instruments = await self.session.execute(
            select(Instrument).where(
                Instrument.code.in_(parsed_codes), Instrument.is_active == True
            )
        )
        existing_instruments = {i.code: i for i in existing_instruments.scalars()}

        # Filter records to only include those with existing instruments
        filtered_records = []
        for record in records:
            parsed_code = record.get("parsed_code")
            if parsed_code and parsed_code in existing_instruments:
                record["instrument_id"] = existing_instruments[parsed_code].id
                filtered_records.append(record)
            else:
                logging.debug(
                    f"No existing instrument found for code {parsed_code}, ignoring record"
                )

        records = filtered_records

        # Get existing snapshots from database
        existing_snapshots = await self.session.execute(
            select(Snapshots).where(Snapshots.code.in_(parsed_codes))
        )
        existing_snapshots = {i.code: i for i in existing_snapshots.scalars()}

        # Process API data and map fields
        update_count = 0
        insert_count = 0

        for record in records:
            parsed_code = record.get("parsed_code")
            if not parsed_code:
                continue

            existing = existing_snapshots.get(parsed_code)

            # Map AkShare fields to snapshots fields
            mapped_record = {
                "name_cn": record.get("名称"),
                "latest_price": record.get("最新价"),
                "change_amount": record.get("涨跌额"),
                "change_percent": record.get("涨跌幅"),
                "open_price": record.get("开盘价"),
                "high_price": record.get("最高价"),
                "low_price": record.get("最低价"),
                "previous_close": record.get("昨收价"),
                "market_cap": record.get("总市值"),
                "pe_ratio": record.get("市盈率"),
                "volume": record.get("成交量"),
                "turnover": record.get("成交额"),
                "amplitude": record.get("振幅"),
                "turnover_rate": record.get("换手率"),
                "code": parsed_code,
            }

            if existing:
                existing.upsert(mapped_record)
                update_count += 1
            else:
                new_snapshot = Snapshots()
                new_snapshot.instrument_id = record["instrument_id"]
                new_snapshot.market = self.market
                new_snapshot.upsert(mapped_record)
                self.session.add(new_snapshot)
                insert_count += 1

        try:
            await self.session.commit()
            logging.info(
                f"Inserted {insert_count} new snapshots, updated {update_count} existing snapshots in snapshots table"
            )
            return insert_count + update_count
        except Exception as e:
            await self.session.rollback()
            logging.error(f"Failed to upsert snapshots records: {str(e)}")
            return 0
