import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.infrastructure.akshare_api.historical_data_api import (
    GetStockHistoricalData,
    _calculate_date_difference,
    _determine_period,
    _detect_market,
    _format_a_stock_historical_data,
    _format_us_stock_historical_data,
    _format_hk_stock_historical_data
)


class TestGetStockHistoricalData:
    """Test cases for GetStockHistoricalData function."""

    def test_get_stock_historical_data_a_stock_success(self):
        """Test GetStockHistoricalData with successful A stock API call."""
        # Create mock DataFrame for A stock
        mock_df = pd.DataFrame({
            '日期': ['2023-01-03', '2023-01-04'],
            '股票代码': ['000001', '000001'],
            '开盘': [10.5, 10.6],
            '收盘': [10.8, 10.7],
            '最高': [11.0, 10.9],
            '最低': [10.4, 10.5],
            '成交量': [1000000, 1200000],
            '成交额': [10800000, 12840000],
            '振幅': [5.71, 3.77],
            '涨跌幅': [2.86, -0.93],
            '涨跌额': [0.3, -0.1],
            '换手率': [1.2, 1.4]
        })

        with patch('app.infrastructure.akshare_api.historical_data_api.ak') as mock_ak:
            mock_ak.stock_zh_a_hist.return_value = mock_df

            result = GetStockHistoricalData(
                symbol="000001",
                start_date="20230101",
                end_date="20230131",
                adjust="qfq",
                period="daily"
            )

            assert result["symbol"] == "000001"
            assert result["market"] == "A"
            assert result["period"] == "daily"
            assert result["adjust"] == "qfq"
            assert result["total_records"] == 2
            assert len(result["data"]) == 2
            assert "units" in result

            mock_ak.stock_zh_a_hist.assert_called_once_with(
                symbol="000001",
                period="daily",
                start_date="20230101",
                end_date="20230131",
                adjust="qfq"
            )

    def test_get_stock_historical_data_us_stock_success(self):
        """Test GetStockHistoricalData with successful US stock API call."""
        # Create mock DataFrame for US stock
        mock_df = pd.DataFrame({
            'date': ['2023-01-03', '2023-01-04'],
            'open': [150.5, 151.0],
            'high': [152.0, 152.5],
            'low': [149.5, 150.0],
            'close': [151.5, 151.2],
            'volume': [5000000, 4800000]
        })

        with patch('app.infrastructure.akshare_api.historical_data_api.ak') as mock_ak:
            mock_ak.stock_us_daily.return_value = mock_df

            result = GetStockHistoricalData(
                symbol="AAPL",
                start_date="20230101",
                end_date="20230131",
                adjust=""
            )

            assert result["symbol"] == "AAPL"
            assert result["market"] == "US"
            assert result["period"] == "daily"  # US stocks only have daily data
            assert result["total_records"] == 2
            assert len(result["data"]) == 2
            assert result["units"]["open"] == "美元"

            mock_ak.stock_us_daily.assert_called_once_with(
                symbol="AAPL",
                adjust=""
            )

    def test_get_stock_historical_data_hk_stock_success(self):
        """Test GetStockHistoricalData with successful HK stock API call."""
        # Create mock DataFrame for HK stock
        mock_df = pd.DataFrame({
            '日期': ['2023-01-03', '2023-01-04'],
            '开盘': [350.0, 352.0],
            '收盘': [355.0, 353.5],
            '最高': [358.0, 356.0],
            '最低': [348.0, 350.0],
            '成交量': [2000000, 1800000],
            '成交额': [710000000, 635400000],
            '振幅': [2.86, 1.70],
            '涨跌幅': [1.43, -0.42],
            '涨跌额': [5.0, -1.5],
            '换手率': [0.5, 0.45]
        })

        with patch('app.infrastructure.akshare_api.historical_data_api.ak') as mock_ak:
            mock_ak.stock_hk_hist.return_value = mock_df

            result = GetStockHistoricalData(
                symbol="00700",
                start_date="20230101",
                end_date="20230131",
                adjust="",
                period="daily"
            )

            assert result["symbol"] == "00700"
            assert result["market"] == "HK"
            assert result["period"] == "daily"
            assert result["total_records"] == 2
            assert len(result["data"]) == 2
            assert result["units"]["open"] == "港元"

            mock_ak.stock_hk_hist.assert_called_once_with(
                symbol="00700",
                period="daily",
                start_date="20230101",
                end_date="20230131",
                adjust=""
            )

    def test_get_stock_historical_data_auto_period_selection(self):
        """Test GetStockHistoricalData with automatic period selection."""
        # Test daily period (less than 30 days)
        with patch('app.infrastructure.akshare_api.historical_data_api.ak') as mock_ak:
            mock_ak.stock_zh_a_hist.return_value = pd.DataFrame({
                '日期': ['2023-01-03'],
                '股票代码': ['000001'],
                '开盘': [10.5], '收盘': [10.8], '最高': [11.0], '最低': [10.4],
                '成交量': [1000000], '成交额': [10800000], '振幅': [5.71],
                '涨跌幅': [2.86], '涨跌额': [0.3], '换手率': [1.2]
            })

            result = GetStockHistoricalData(
                symbol="000001",
                start_date="20230101",
                end_date="20230115",  # 15 days difference
                period="auto"
            )

            assert result["period"] == "daily"

        # Test weekly period (more than 30 days)
        with patch('app.infrastructure.akshare_api.historical_data_api.ak') as mock_ak:
            mock_ak.stock_zh_a_hist.return_value = pd.DataFrame({
                '日期': ['2023-01-03'],
                '股票代码': ['000001'],
                '开盘': [10.5], '收盘': [10.8], '最高': [11.0], '最低': [10.4],
                '成交量': [1000000], '成交额': [10800000], '振幅': [5.71],
                '涨跌幅': [2.86], '涨跌额': [0.3], '换手率': [1.2]
            })

            result = GetStockHistoricalData(
                symbol="000001",
                start_date="20230101",
                end_date="20230301",  # 60 days difference
                period="auto"
            )

            assert result["period"] == "weekly"

        # Test monthly period (more than 365 days)
        with patch('app.infrastructure.akshare_api.historical_data_api.ak') as mock_ak:
            mock_ak.stock_zh_a_hist.return_value = pd.DataFrame({
                '日期': ['2023-01-03'],
                '股票代码': ['000001'],
                '开盘': [10.5], '收盘': [10.8], '最高': [11.0], '最低': [10.4],
                '成交量': [1000000], '成交额': [10800000], '振幅': [5.71],
                '涨跌幅': [2.86], '涨跌额': [0.3], '换手率': [1.2]
            })

            result = GetStockHistoricalData(
                symbol="000001",
                start_date="20220101",
                end_date="20230102",  # 366 days difference to ensure > 365
                period="auto"
            )

            assert result["period"] == "monthly"

    def test_get_stock_historical_data_empty_response(self):
        """Test GetStockHistoricalData with empty API response."""
        with patch('app.infrastructure.akshare_api.historical_data_api.ak') as mock_ak:
            mock_ak.stock_zh_a_hist.return_value = pd.DataFrame()

            result = GetStockHistoricalData(
                symbol="000001",
                start_date="20230101",
                end_date="20230131"
            )

            assert "error" in result
            assert result["symbol"] == "000001"
            assert result["start_date"] == "20230101"
            assert result["end_date"] == "20230131"

    def test_get_stock_historical_data_api_error(self):
        """Test GetStockHistoricalData handles API errors."""
        with patch('app.infrastructure.akshare_api.historical_data_api.ak') as mock_ak:
            mock_ak.stock_zh_a_hist.side_effect = Exception("API Error")

            result = GetStockHistoricalData(
                symbol="000001",
                start_date="20230101",
                end_date="20230131"
            )

            assert "error" in result
            assert "API Error" in result["error"]
            assert result["symbol"] == "000001"

    def test_get_stock_historical_data_empty_symbol(self):
        """Test GetStockHistoricalData with empty stock symbol."""
        with pytest.raises(ValueError) as exc_info:
            GetStockHistoricalData(
                symbol="",
                start_date="20230101",
                end_date="20230131"
            )

        assert "股票代码不能为空" in str(exc_info.value)

    def test_get_stock_historical_data_empty_dates(self):
        """Test GetStockHistoricalData with empty dates."""
        with pytest.raises(ValueError) as exc_info:
            GetStockHistoricalData(
                symbol="000001",
                start_date="",
                end_date="20230131"
            )

        assert "开始日期和结束日期不能为空" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            GetStockHistoricalData(
                symbol="000001",
                start_date="20230101",
                end_date=""
            )

        assert "开始日期和结束日期不能为空" in str(exc_info.value)

    def test_get_stock_historical_data_invalid_date_format(self):
        """Test GetStockHistoricalData with invalid date format."""
        with pytest.raises(ValueError) as exc_info:
            GetStockHistoricalData(
                symbol="000001",
                start_date="2023-01-01",  # Wrong format
                end_date="20230131"
            )

        assert "日期格式不正确" in str(exc_info.value)

    def test_get_stock_historical_data_invalid_adjust(self):
        """Test GetStockHistoricalData with invalid adjust parameter."""
        with pytest.raises(ValueError) as exc_info:
            GetStockHistoricalData(
                symbol="000001",
                start_date="20230101",
                end_date="20230131",
                adjust="invalid_adjust"
            )

        assert "复权类型不正确" in str(exc_info.value)

    def test_get_stock_historical_data_invalid_period(self):
        """Test GetStockHistoricalData with invalid period parameter."""
        with pytest.raises(ValueError) as exc_info:
            GetStockHistoricalData(
                symbol="000001",
                start_date="20230101",
                end_date="20230131",
                period="invalid_period"
            )

        assert "数据频率不正确" in str(exc_info.value)

    def test_get_stock_historical_data_unknown_market(self):
        """Test GetStockHistoricalData with unknown market type."""
        # Test that the function returns an error dict instead of raising exception
        with patch('app.infrastructure.akshare_api.historical_data_api.ak') as mock_ak:
            # Mock any API call to avoid actual errors
            mock_ak.stock_zh_a_hist.return_value = pd.DataFrame()
            
            result = GetStockHistoricalData(
                symbol="123",  # Not matching any market pattern (too short)
                start_date="20230101",
                end_date="20230131"
            )

            assert "error" in result
            assert "无法识别股票代码" in result["error"]


class TestHelperFunctions:
    """Test cases for helper functions in historical_data_api."""

    def test_calculate_date_difference(self):
        """Test _calculate_date_difference function."""
        result = _calculate_date_difference("20230101", "20230131")
        assert result == 30  # 30 days difference

        result = _calculate_date_difference("20230101", "20230101")
        assert result == 0  # Same day

    def test_calculate_date_difference_invalid_format(self):
        """Test _calculate_date_difference with invalid date format."""
        with pytest.raises(ValueError) as exc_info:
            _calculate_date_difference("2023-01-01", "20230131")

        assert "日期格式不正确" in str(exc_info.value)

    def test_determine_period(self):
        """Test _determine_period function."""
        # Daily period (less than 30 days)
        result = _determine_period("20230101", "20230115")
        assert result == "daily"

        # Weekly period (more than 30 days, less than 365 days)
        result = _determine_period("20230101", "20230301")
        assert result == "weekly"

        # Monthly period (more than 365 days)
        result = _determine_period("20220101", "20230102")  # 366 days difference
        assert result == "monthly"

    def test_detect_market(self):
        """Test _detect_market function."""
        # A stock detection
        result = _detect_market("000001")
        assert result == "A"

        result = _detect_market("600000")
        assert result == "A"

        # US stock detection
        result = _detect_market("AAPL")
        assert result == "US"

        result = _detect_market("TSLA")
        assert result == "US"

        # HK stock detection
        result = _detect_market("00700")
        assert result == "HK"

        result = _detect_market("00941")
        assert result == "HK"

    def test_detect_market_unknown(self):
        """Test _detect_market with unknown market type."""
        with pytest.raises(ValueError) as exc_info:
            _detect_market("123")  # Too short, doesn't match any market pattern

        assert "无法识别股票代码" in str(exc_info.value)

    def test_format_a_stock_historical_data(self):
        """Test _format_a_stock_historical_data function."""
        # Create test DataFrame
        test_df = pd.DataFrame({
            '日期': ['2023-01-03', '2023-01-04'],
            '股票代码': ['000001', '000001'],
            '开盘': [10.5, 10.6],
            '收盘': [10.8, 10.7],
            '最高': [11.0, 10.9],
            '最低': [10.4, 10.5],
            '成交量': [1000000, 1200000],
            '成交额': [10800000, 12840000],
            '振幅': [5.71, 3.77],
            '涨跌幅': [2.86, -0.93],
            '涨跌额': [0.3, -0.1],
            '换手率': [1.2, 1.4]
        })

        result = _format_a_stock_historical_data(
            test_df, "000001", "daily", "qfq"
        )

        assert result["symbol"] == "000001"
        assert result["market"] == "A"
        assert result["period"] == "daily"
        assert result["adjust"] == "qfq"
        assert result["total_records"] == 2
        assert len(result["data"]) == 2
        assert "units" in result
        assert result["units"]["open"] == "元"

        # Check field mapping
        assert "date" in result["data"][0]
        assert "open" in result["data"][0]
        assert "close" in result["data"][0]

    def test_format_us_stock_historical_data(self):
        """Test _format_us_stock_historical_data function."""
        # Create test DataFrame
        test_df = pd.DataFrame({
            'date': ['2023-01-03', '2023-01-04'],
            'open': [150.5, 151.0],
            'high': [152.0, 152.5],
            'low': [149.5, 150.0],
            'close': [151.5, 151.2],
            'volume': [5000000, 4800000]
        })

        result = _format_us_stock_historical_data(
            test_df, "AAPL", ""
        )

        assert result["symbol"] == "AAPL"
        assert result["market"] == "US"
        assert result["period"] == "daily"
        assert result["adjust"] == ""
        assert result["total_records"] == 2
        assert len(result["data"]) == 2
        assert result["units"]["open"] == "美元"

    def test_format_hk_stock_historical_data(self):
        """Test _format_hk_stock_historical_data function."""
        # Create test DataFrame
        test_df = pd.DataFrame({
            '日期': ['2023-01-03', '2023-01-04'],
            '开盘': [350.0, 352.0],
            '收盘': [355.0, 353.5],
            '最高': [358.0, 356.0],
            '最低': [348.0, 350.0],
            '成交量': [2000000, 1800000],
            '成交额': [710000000, 635400000],
            '振幅': [2.86, 1.70],
            '涨跌幅': [1.43, -0.42],
            '涨跌额': [5.0, -1.5],
            '换手率': [0.5, 0.45]
        })

        result = _format_hk_stock_historical_data(
            test_df, "00700", "daily", ""
        )

        assert result["symbol"] == "00700"
        assert result["market"] == "HK"
        assert result["period"] == "daily"
        assert result["adjust"] == ""
        assert result["total_records"] == 2
        assert len(result["data"]) == 2
        assert result["units"]["open"] == "港元"

        # Check field mapping
        assert "date" in result["data"][0]
        assert "open" in result["data"][0]
        assert "close" in result["data"][0]


if __name__ == "__main__":
    pytest.main([__file__])
