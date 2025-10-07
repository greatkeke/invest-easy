import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.infrastructure.akshare_api.snapshot_api import GetStockSpotData


class TestGetStockSpotData:
    """Test cases for GetStockSpotData function."""

    def test_get_stock_spot_data_success(self):
        """Test GetStockSpotData with successful API call."""
        # Create mock DataFrame for stock spot data
        mock_df = pd.DataFrame({
            'item': [
                '代码', '名称', '现价', '涨跌', '涨幅', '今开', '最高', '最低', '昨收',
                '成交量', '成交额', '振幅', '周转率', '市盈率(动)', '市净率', '基金份额/总股本',
                '流通股', '52周最高', '52周最低', '时间'
            ],
            'value': [
                '000001', '平安银行', 15.80, 0.32, 2.07, 15.50, 15.90, 15.45, 15.48,
                50000000, 790000000, 2.91, 1.25, 8.5, 0.85, 2000000000, 1500000000,
                16.20, 12.50, '2023-10-07 11:00:00'
            ]
        })

        with patch('app.infrastructure.akshare_api.snapshot_api.ak') as mock_ak:
            mock_ak.stock_individual_spot_xq.return_value = mock_df

            result = GetStockSpotData(symbol="000001")

            assert result["symbol"] == "000001"
            assert result["name"] == "平安银行"
            assert result["current_price"] == 15.80
            assert result["change_amount"] == 0.32
            assert result["change_percent"] == 2.07
            assert result["open"] == 15.50
            assert result["high"] == 15.90
            assert result["low"] == 15.45
            assert result["previous_close"] == 15.48
            assert result["volume"] == 50000000
            assert result["turnover"] == 790000000
            assert result["amplitude"] == 2.91
            assert result["turnover_rate"] == 1.25
            assert result["pe_dynamic"] == 8.5
            assert result["pb_ratio"] == 0.85
            assert result["total_shares"] == 2000000000
            assert result["circulating_shares"] == 1500000000
            assert result["week_52_high"] == 16.20
            assert result["week_52_low"] == 12.50
            assert result["timestamp"] == '2023-10-07 11:00:00'

            # Check units
            assert "units" in result
            assert result["units"]["current_price"] == "元"
            assert result["units"]["change_amount"] == "元"
            assert result["units"]["change_percent"] == "%"
            assert result["units"]["volume"] == "股"

            mock_ak.stock_individual_spot_xq.assert_called_once_with(
                symbol="000001"
            )


if __name__ == "__main__":
    pytest.main([__file__])
