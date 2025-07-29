import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infrastructure.akshare_service import AkshareService
from app.domain.snapshots import Snapshots
from app.domain.instruments import Instrument
import pandas as pd
import numpy as np


class TestAkshareService:
    """Test cases for AkshareService class."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        return AsyncMock(spec=AsyncSession)

    @pytest.fixture
    def akshare_service(self, mock_session):
        """Create an instance of AkshareService with mocked session."""
        return AkshareService(session=mock_session)

    def test_parse_code(self, akshare_service):
        """Test _parse_code method."""
        # Test normal code parsing
        result = akshare_service._parse_code("105.DBGI")
        assert result == "US.DBGI"

        # Test code without dot
        result = akshare_service._parse_code("DBGI")
        assert result == "US.DBGI"

        # Test empty code
        result = akshare_service._parse_code("")
        assert result == ""

        # Test None code
        result = akshare_service._parse_code(None)
        assert result is None

    @patch("app.infrastructure.akshare_service.ak")
    def test_get_us_stock_spot_success(self, mock_ak, akshare_service):
        """Test get_us_stock_spot method with successful API call."""
        # Create mock DataFrame
        mock_df = pd.DataFrame(
            {
                "代码": ["105.DBGI", "106.AAPL"],
                "名称": ["股票A", "股票B"],
                "最新价": [100.0, 150.0],
                "涨跌额": [1.0, -0.5],
            }
        )
        mock_ak.stock_us_spot_em.return_value = mock_df

        result = akshare_service.get_us_stock_spot()

        assert len(result) == 2
        assert result[0]["代码"] == "105.DBGI"
        assert result[1]["代码"] == "106.AAPL"
        mock_ak.stock_us_spot_em.assert_called_once()

    @patch("app.infrastructure.akshare_service.ak")
    def test_get_us_stock_spot_with_nan_values(self, mock_ak, akshare_service):
        """Test get_us_stock_spot method handles NaN values."""
        # Create mock DataFrame with NaN values
        mock_df = pd.DataFrame(
            {
                "代码": ["105.DBGI"],
                "名称": ["股票A"],
                "最新价": [np.nan],
                "涨跌额": [1.0],
            }
        )
        mock_ak.stock_us_spot_em.return_value = mock_df

        result = akshare_service.get_us_stock_spot()

        assert len(result) == 1
        assert result[0]["最新价"] is None  # NaN should be converted to None
        assert result[0]["涨跌额"] == 1.0

    @patch("app.infrastructure.akshare_service.ak")
    def test_get_us_stock_spot_api_error(self, mock_ak, akshare_service):
        """Test get_us_stock_spot method handles API errors."""
        mock_ak.stock_us_spot_em.side_effect = Exception("API Error")

        with pytest.raises(RuntimeError) as exc_info:
            akshare_service.get_us_stock_spot()

        assert "AkShare API error" in str(exc_info.value)

    @patch("app.infrastructure.akshare_service.ak")
    @pytest.mark.asyncio
    async def test_initialize_snapshots_table_recent_update(
        self, mock_ak, mock_session, akshare_service
    ):
        """Test initialize_snapshots_table when data is recent (less than 1 day old)."""
        # Mock recent update time
        recent_time = datetime.now()
        # Create a proper async mock for the execute result
        mock_session.execute.side_effect = [
            AsyncMock(
                scalar_one_or_none=lambda: recent_time
            ),  # First call for update time
        ]

        result = await akshare_service.initialize_snapshots_table()

        assert result == 0
        mock_session.execute.assert_called()
        mock_ak.stock_us_spot_em.assert_not_called()

    @patch("app.infrastructure.akshare_service.ak")
    @pytest.mark.asyncio
    async def test_initialize_snapshots_table_no_data(
        self, mock_ak, mock_session, akshare_service
    ):
        """Test initialize_snapshots_table when no data is returned from API."""
        # Mock old update time
        old_time = datetime.now() - timedelta(days=2)
        # Create a proper async mock for the execute result
        mock_session.execute.side_effect = [
            AsyncMock(
                scalar_one_or_none=lambda: old_time
            ),  # First call for update time
        ]

        # Mock empty API response
        mock_ak.stock_us_spot_em.return_value = pd.DataFrame()

        result = await akshare_service.initialize_snapshots_table()

        assert result == 0
        mock_ak.stock_us_spot_em.assert_called_once()

    @patch("app.infrastructure.akshare_service.ak")
    @pytest.mark.asyncio
    async def test_initialize_snapshots_table_success(
        self, mock_ak, mock_session, akshare_service
    ):
        """Test initialize_snapshots_table with successful data processing."""
        # Mock old update time
        old_time = datetime.now() - timedelta(days=2)
        mock_session.execute.return_value.scalar_one_or_none.return_value = old_time

        # Mock API response
        mock_df = pd.DataFrame(
            {
                "代码": ["105.DBGI", "106.AAPL"],
                "名称": ["股票A", "股票B"],
                "最新价": [100.0, 150.0],
                "涨跌额": [1.0, -0.5],
                "涨跌幅": [1.0, -0.33],
                "开盘价": [99.0, 151.0],
                "最高价": [101.0, 152.0],
                "最低价": [98.0, 149.0],
                "昨收价": [99.0, 150.5],
                "总市值": [1000000.0, 2000000.0],
                "市盈率": [15.0, 20.0],
                "成交量": [1000.0, 2000.0],
                "成交额": [100000.0, 300000.0],
                "振幅": [3.0, 2.0],
                "换手率": [0.1, 0.2],
            }
        )
        mock_ak.stock_us_spot_em.return_value = mock_df

        # Mock existing instruments
        mock_instrument1 = Mock(spec=Instrument)
        mock_instrument1.id = "instrument_id_1"
        mock_instrument1.code = "US.DBGI"

        mock_instrument2 = Mock(spec=Instrument)
        mock_instrument2.id = "instrument_id_2"
        mock_instrument2.code = "US.AAPL"

        mock_session.execute.side_effect = [
            AsyncMock(
                scalar_one_or_none=lambda: old_time
            ),  # First call for update time
            AsyncMock(
                scalars=lambda: [mock_instrument1, mock_instrument2]
            ),  # Instruments query
            AsyncMock(scalars=lambda: []),  # Snapshots query (empty for new inserts)
        ]

        result = await akshare_service.initialize_snapshots_table()

        assert result == 2  # 2 records inserted
        mock_session.commit.assert_called_once()
        assert mock_session.add.call_count == 2  # 2 new snapshots added

    @patch("app.infrastructure.akshare_service.ak")
    @pytest.mark.asyncio
    async def test_initialize_snapshots_table_with_updates(
        self, mock_ak, mock_session, akshare_service
    ):
        """Test initialize_snapshots_table with existing snapshots that need updating."""
        # Mock old update time
        old_time = datetime.now() - timedelta(days=2)
        mock_session.execute.return_value.scalar_one_or_none.return_value = old_time

        # Mock API response
        mock_df = pd.DataFrame(
            {
                "代码": ["105.DBGI"],
                "名称": ["股票A"],
                "最新价": [100.0],
                "涨跌额": [1.0],
                "涨跌幅": [1.0],
                "开盘价": [99.0],
                "最高价": [101.0],
                "最低价": [98.0],
                "昨收价": [99.0],
                "总市值": [1000000.0],
                "市盈率": [15.0],
                "成交量": [1000.0],
                "成交额": [100000.0],
                "振幅": [3.0],
                "换手率": [0.1],
            }
        )
        mock_ak.stock_us_spot_em.return_value = mock_df

        # Mock existing instrument
        mock_instrument = Mock(spec=Instrument)
        mock_instrument.id = "instrument_id_1"
        mock_instrument.code = "US.DBGI"

        # Mock existing snapshot
        mock_snapshot = Mock(spec=Snapshots)
        mock_snapshot.code = "US.DBGI"
        mock_snapshot.upsert = Mock()

        mock_session.execute.side_effect = [
            AsyncMock(
                scalar_one_or_none=lambda: old_time
            ),  # First call for update time
            AsyncMock(scalars=lambda: [mock_instrument]),  # Instruments query
            AsyncMock(scalars=lambda: [mock_snapshot]),  # Snapshots query
        ]

        result = await akshare_service.initialize_snapshots_table()

        assert result == 1  # 1 record updated
        mock_session.commit.assert_called_once()
        mock_snapshot.upsert.assert_called_once()
        mock_session.add.assert_not_called()  # No new snapshots added

    @patch("app.infrastructure.akshare_service.ak")
    @pytest.mark.asyncio
    async def test_initialize_snapshots_table_api_error(
        self, mock_ak, mock_session, akshare_service
    ):
        """Test initialize_snapshots_table handles API errors."""
        # Mock old update time
        old_time = datetime.now() - timedelta(days=2)
        # Create a proper async mock for the execute result
        mock_session.execute.side_effect = [
            AsyncMock(
                scalar_one_or_none=lambda: old_time
            ),  # First call for update time
        ]

        # Mock API error
        mock_ak.stock_us_spot_em.side_effect = Exception("API Error")

        result = await akshare_service.initialize_snapshots_table()

        assert result == 0


    @patch("app.infrastructure.akshare_service.ak")
    @pytest.mark.asyncio
    async def test_initialize_snapshots_table_db_error(
        self, mock_ak, mock_session, akshare_service
    ):
        """Test initialize_snapshots_table handles database errors."""
        # Mock old update time
        old_time = datetime.now() - timedelta(days=2)

        # Mock database commit error
        mock_session.commit.side_effect = Exception("DB Error")

        # Mock some data to trigger commit
        mock_df = pd.DataFrame({"代码": ["105.DBGI"], "名称": ["股票A"]})
        mock_ak.stock_us_spot_em.return_value = mock_df

        # Mock existing instrument
        mock_instrument = Mock(spec=Instrument)
        mock_instrument.id = "instrument_id_1"
        mock_instrument.code = "US.DBGI"

        mock_session.execute.side_effect = [
            AsyncMock(
                scalar_one_or_none=lambda: old_time
            ),  # First call for update time
            AsyncMock(scalars=lambda: [mock_instrument]),  # Instruments query
            AsyncMock(scalars=lambda: []),  # Snapshots query
        ]

        # with pytest.raises(Exception) as exc_info:
        #     await akshare_service.initialize_snapshots_table()

        # assert "DB Error" in str(exc_info.value)
        result = await akshare_service.initialize_snapshots_table()
        mock_session.rollback.assert_called_once()
        assert result == 0


if __name__ == "__main__":
    pytest.main([__file__])
