import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.market_service import MarketService
from app.infrastructure.futu_api_service import FutuApiService
from app.infrastructure.akshare_service import AkshareService
from app.services.watchlist_service import WatchlistService
from app.domain.snapshots import Snapshots


class TestMarketService:
    """Test cases for MarketService class."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        return AsyncMock(spec=AsyncSession)

    @pytest.fixture
    def mock_futu_service(self):
        """Create a mock Futu API service."""
        return Mock(spec=FutuApiService)

    @pytest.fixture
    def mock_akshare_service(self):
        """Create a mock Akshare service."""
        return Mock(spec=AkshareService)

    @pytest.fixture
    def mock_watchlist_service(self):
        """Create a mock watchlist service."""
        return Mock(spec=WatchlistService)

    @pytest.fixture
    def market_service(self, mock_futu_service, mock_akshare_service, mock_watchlist_service, mock_session):
        """Create an instance of MarketService with mocked dependencies."""
        return MarketService(
            futu_api_svc=mock_futu_service,
            akshare_svc=mock_akshare_service,
            watch_list_svc=mock_watchlist_service,
            session=mock_session
        )

    def test_get_market_snapshot_empty_list(self, market_service):
        """Test get_market_snapshot with empty code list."""
        result = asyncio.run(market_service.get_market_snapshot([]))
        assert result == []

    @patch('app.services.market_service.select')
    def test_get_market_snapshot_us_codes_only(self, mock_select, market_service, mock_session):
        """Test get_market_snapshot with US codes only."""
        # Mock database response
        mock_snapshot = Mock(spec=Snapshots)
        mock_snapshot.futu_code = "US.AAPL"
        mock_snapshot.latest_price = 150.0
        mock_snapshot.change_percent = 1.0
        mock_snapshot.change_amount = 1.5
        
        mock_exec = Mock()
        mock_exec.all.return_value = [(mock_snapshot, "Apple")]
        mock_session.execute.return_value = mock_exec

        code_list = ["US.AAPL", "US.GOOG"]
        result = asyncio.run(market_service.get_market_snapshot(code_list))

        assert len(result) == 1
        assert result[0]['code'] == "US.AAPL"
        assert result[0]['name'] == "Apple"
        assert result[0]['last_price'] == 150.0
        mock_session.execute.assert_called_once()

    def test_get_market_snapshot_non_us_codes_only(self, market_service, mock_futu_service):
        """Test get_market_snapshot with non-US codes only."""
        # Mock Futu API response
        mock_futu_response = [
            {
                'code': 'HK.00700',
                'name': 'Tencent',
                'last_price': 300.0,
                'change_rate': 2.0
            }
        ]
        mock_futu_service.get_market_snapshot.return_value = mock_futu_response

        code_list = ["HK.00700", "SH.600000"]
        result = asyncio.run(market_service.get_market_snapshot(code_list))

        assert len(result) == 1
        assert result[0]['code'] == 'HK.00700'
        assert result[0]['name'] == 'Tencent'
        mock_futu_service.get_market_snapshot.assert_called_once_with(code_list=code_list)

    def test_get_market_snapshot_mixed_codes(self, market_service, mock_futu_service, mock_session):
        """Test get_market_snapshot with mixed US and non-US codes."""
        # Mock database response for US codes
        mock_snapshot = Mock(spec=Snapshots)
        mock_snapshot.futu_code = "US.AAPL"
        mock_snapshot.latest_price = 150.0
        mock_snapshot.change_percent = 1.0
        
        mock_db_result = Mock()
        mock_db_result.all.return_value = [(mock_snapshot, "Apple")]
        mock_session.execute.return_value = mock_db_result

        # Mock Futu API response for non-US codes
        mock_futu_response = [
            {
                'code': 'HK.00700',
                'name': 'Tencent',
                'last_price': 300.0,
                'change_rate': 2.0
            }
        ]
        mock_futu_service.get_market_snapshot.return_value = mock_futu_response

        code_list = ["US.AAPL", "HK.00700"]
        result = asyncio.run(market_service.get_market_snapshot(code_list))

        assert len(result) == 2
        # Check that both US and non-US data are present
        codes = [item['code'] for item in result]
        assert "US.AAPL" in codes
        assert "HK.00700" in codes

    @patch('app.services.market_service.select')
    def test_get_market_snapshot_db_error(self, mock_select, market_service, mock_session, mock_futu_service):
        """Test get_market_snapshot handles database errors gracefully."""
        # Mock database error
        mock_session.execute.side_effect = Exception("Database error")
        
        # Mock Futu API response
        mock_futu_response = [
            {
                'code': 'HK.00700',
                'name': 'Tencent',
                'last_price': 300.0
            }
        ]
        mock_futu_service.get_market_snapshot.return_value = mock_futu_response

        code_list = ["US.AAPL", "HK.00700"]
        result = asyncio.run(market_service.get_market_snapshot(code_list))

        # Should still return non-US data even if US data fails
        assert len(result) == 1
        assert result[0]['code'] == 'HK.00700'

    def test_get_market_snapshot_futu_error(self, market_service, mock_futu_service, mock_session):
        """Test get_market_snapshot handles Futu API errors gracefully."""
        # Mock database response for US codes
        mock_snapshot = Mock(spec=Snapshots)
        mock_snapshot.futu_code = "US.AAPL"
        mock_snapshot.latest_price = 150.0
        
        mock_db_result = Mock()
        mock_db_result.all.return_value = [(mock_snapshot, "Apple")]
        mock_session.execute.return_value = mock_db_result

        # Mock Futu API error
        mock_futu_service.get_market_snapshot.side_effect = Exception("Futu API error")

        code_list = ["US.AAPL", "HK.00700"]
        result = asyncio.run(market_service.get_market_snapshot(code_list))

        # Should still return US data even if non-US data fails
        assert len(result) == 1
        assert result[0]['code'] == "US.AAPL"

    @patch('app.services.market_service.select')
    def test_get_rt_data_us_stock_success(self, mock_select, market_service, mock_akshare_service, mock_session):
        """Test get_rt_data for US stock with successful database lookup and akshare call."""
        # Mock database response
        mock_snapshot = Mock(spec=Snapshots)
        mock_snapshot.code = "105.AAPL"  # Raw symbol code for akshare
        
        mock_exec = Mock()
        mock_exec.scalar_one_or_none.return_value = mock_snapshot
        mock_session.execute.return_value = mock_exec

        # Mock akshare response
        mock_rt_data = [
            {
                "time": "2023-01-01 10:00:00",
                "open": 150.0,
                "close": 151.0,
                "high": 152.0,
                "low": 149.0,
                "volume": 1000,
                "turnover": 150000,
                "cur_price": 151.0
            }
        ]
        mock_akshare_service.get_rtdata.return_value = mock_rt_data

        result = asyncio.run(market_service.get_rt_data("US.AAPL"))

        assert result == mock_rt_data
        mock_session.execute.assert_called_once()
        mock_akshare_service.get_rtdata.assert_called_once_with(symbol="105.AAPL")

    @patch('app.services.market_service.select')
    def test_get_rt_data_us_stock_no_snapshot(self, mock_select, market_service, mock_futu_service, mock_session):
        """Test get_rt_data for US stock when no snapshot found in database."""
        # Mock database response - no snapshot found
        mock_exec = Mock()
        mock_exec.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_exec

        # Mock Futu API response (fallback)
        mock_rt_data = []
        mock_futu_service.get_rt_data.return_value = mock_rt_data

        result = asyncio.run(market_service.get_rt_data("US.AAPL"))

        assert result == mock_rt_data
        mock_session.execute.assert_called_once()

    @patch('app.services.market_service.select')
    def test_get_rt_data_us_stock_db_error(self, mock_select, market_service, mock_futu_service, mock_session):
        """Test get_rt_data for US stock when database query fails."""
        # Mock database error
        mock_session.execute.side_effect = Exception("Database error")

        # Mock Futu API response (fallback)
        mock_rt_data = []
        mock_futu_service.get_rt_data.return_value = mock_rt_data

        result = asyncio.run(market_service.get_rt_data("US.AAPL"))

        assert result == mock_rt_data
        mock_session.execute.assert_called_once()

    @patch('app.services.market_service.select')
    def test_get_rt_data_us_stock_akshare_error(self, mock_select, market_service, mock_akshare_service, mock_futu_service, mock_session):
        """Test get_rt_data for US stock when akshare call fails."""
        # Mock database response
        mock_snapshot = Mock(spec=Snapshots)
        mock_snapshot.code = "105.AAPL"
        
        mock_exec = Mock()
        mock_exec.scalar_one_or_none.return_value = mock_snapshot
        mock_session.execute.return_value = mock_exec

        # Mock akshare error
        mock_akshare_service.get_rtdata.side_effect = Exception("Akshare error")

        # Mock Futu API response (fallback)
        mock_rt_data = []
        mock_futu_service.get_rt_data.return_value = mock_rt_data

        result = asyncio.run(market_service.get_rt_data("US.AAPL"))

        assert result == mock_rt_data
        mock_session.execute.assert_called_once()
        mock_akshare_service.get_rtdata.assert_called_once_with(symbol="105.AAPL")

    def test_get_rt_data_non_us_stock(self, market_service, mock_futu_service):
        """Test get_rt_data for non-US stock (should use Futu API directly)."""
        # Mock Futu API response
        mock_rt_data = [{"time": "2023-01-01 10:00:00", "price": 300.0}]
        mock_futu_service.get_rt_data.return_value = mock_rt_data

        result = asyncio.run(market_service.get_rt_data("HK.00700"))

        assert result == mock_rt_data
        mock_futu_service.get_rt_data.assert_called_once_with(code="HK.00700")


if __name__ == "__main__":
    pytest.main([__file__])
