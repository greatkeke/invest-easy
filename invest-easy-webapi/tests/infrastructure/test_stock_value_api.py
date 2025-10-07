import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.infrastructure.akshare_api.stock_value_api import GetStockValue


class TestGetStockValue:
    """Test cases for GetStockValue function."""

    def test_get_stock_value_success(self):
        """Test GetStockValue with successful API call."""
        # Create mock DataFrame for stock valuation data
        mock_df = pd.DataFrame({
            '数据日期': ['2023-10-07', '2023-10-06'],
            '当日收盘价': [15.80, 15.48],
            '当日涨跌幅': [2.07, -1.25],
            '总市值': [31600000000.0, 30960000000.0],
            '流通市值': [23700000000.0, 23220000000.0],
            '总股本': [2000000000, 2000000000],
            '流通股本': [1500000000, 1500000000],
            'PE(TTM)': [8.5, 8.3],
            'PE(静)': [8.2, 8.0],
            '市净率': [0.85, 0.83],
            'PEG值': [0.75, 0.73],
            '市现率': [6.8, 6.6],
            '市销率': [1.2, 1.18]
        })

        with patch('app.infrastructure.akshare_api.stock_value_api.ak') as mock_ak:
            mock_ak.stock_value_em.return_value = mock_df

            result = GetStockValue(symbol="000001")

            assert result["symbol"] == "000001"
            assert result["date"] == "2023-10-06"  # 获取的是最后一行数据
            assert result["close_price"] == 15.48
            assert result["change_percent"] == -1.25
            assert result["total_market_cap"] == 30960000000.0
            assert result["circulating_market_cap"] == 23220000000.0
            assert result["total_shares"] == 2000000000
            assert result["circulating_shares"] == 1500000000
            assert result["pe_ttm"] == 8.3
            assert result["pe_static"] == 8.0
            assert result["pb_ratio"] == 0.83
            assert result["peg_ratio"] == 0.73
            assert result["pcf_ratio"] == 6.6
            assert result["ps_ratio"] == 1.18

            # Check units
            assert "units" in result
            assert result["units"]["close_price"] == "元"
            assert result["units"]["change_percent"] == "%"
            assert result["units"]["total_market_cap"] == "元"
            assert result["units"]["circulating_market_cap"] == "元"
            assert result["units"]["total_shares"] == "股"
            assert result["units"]["circulating_shares"] == "股"
            assert result["units"]["pe_ttm"] == "倍"
            assert result["units"]["pe_static"] == "倍"
            assert result["units"]["pb_ratio"] == "倍"
            assert result["units"]["peg_ratio"] == "倍"
            assert result["units"]["pcf_ratio"] == "倍"
            assert result["units"]["ps_ratio"] == "倍"

            mock_ak.stock_value_em.assert_called_once_with(
                symbol="000001"
            )


if __name__ == "__main__":
    pytest.main([__file__])
