import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.infrastructure.akshare_tools import QueryUSStockFinacialReport, _format_financial_report_data


class TestQueryUSStockFinacialReport:
    """Test cases for QueryUSStockFinacialReport function."""

    def test_query_us_stock_financial_report_success(self):
        """Test QueryUSStockFinacialReport with successful API call."""
        # Create mock DataFrame
        mock_df = pd.DataFrame({
            'REPORT_DATE': ['2023-12-31', '2023-12-31'],
            'ITEM_NAME': ['Total Assets', 'Total Liabilities'],
            'AMOUNT': [1000000.0, 500000.0],
            'STD_ITEM_CODE': ['A001', 'L001'],
            'REPORT_TYPE': ['Balance Sheet', 'Balance Sheet'],
            'SECURITY_CODE': ['TSLA', ''],
            'SECURITY_NAME_ABBR': ['Tesla Inc', '']
        })

        with patch('app.infrastructure.akshare_tools.ak') as mock_ak:
            mock_ak.stock_financial_us_report_em.return_value = mock_df

            result = QueryUSStockFinacialReport(
                stock="TSLA",
                symbol="资产负债表",
                indicator="年报"
            )

            assert result["stock"] == "TSLA"
            assert result["symbol"] == "资产负债表"
            assert result["indicator"] == "年报"
            assert result["total_records"] == 2
            assert "2023-12-31" in result["report_dates"]
            assert len(result["report_data"]["2023-12-31"]) == 2

            mock_ak.stock_financial_us_report_em.assert_called_once_with(
                stock="TSLA",
                symbol="资产负债表",
                indicator="年报"
            )

    def test_query_us_stock_financial_report_with_stock_code_conversion(self):
        """Test QueryUSStockFinacialReport with stock code conversion (dot to underscore)."""
        # Create mock DataFrame
        mock_df = pd.DataFrame({
            'REPORT_DATE': ['2023-12-31'],
            'ITEM_NAME': ['Total Assets'],
            'AMOUNT': [1000000.0],
            'STD_ITEM_CODE': ['A001'],
            'REPORT_TYPE': ['Balance Sheet'],
            'SECURITY_CODE': ['BRK_A'],
            'SECURITY_NAME_ABBR': ['Berkshire Hathaway']
        })

        with patch('app.infrastructure.akshare_tools.ak') as mock_ak:
            mock_ak.stock_financial_us_report_em.return_value = mock_df

            result = QueryUSStockFinacialReport(
                stock= "BRK.A",  # Should be converted to BRK_A
                symbol= "资产负债表",
                indicator= "年报"
            )

            assert result.get("stock") == "BRK.A"  # Original stock code
            assert result.get("total_records") == 1

            # Verify the API was called with converted stock code
            mock_ak.stock_financial_us_report_em.assert_called_once_with(
                stock="BRK_A",  # Converted stock code
                symbol="资产负债表",
                indicator="年报"
            )

    def test_query_us_stock_financial_report_different_report_types(self):
        """Test QueryUSStockFinacialReport with different report types."""
        # Create mock DataFrame for income statement
        mock_df = pd.DataFrame({
            'REPORT_DATE': ['2023-12-31'],
            'ITEM_NAME': ['Revenue'],
            'AMOUNT': [500000.0],
            'STD_ITEM_CODE': ['I001'],
            'REPORT_TYPE': ['Income Statement'],
            'SECURITY_CODE': ['AAPL'],
            'SECURITY_NAME_ABBR': ['Apple Inc']
        })

        with patch('app.infrastructure.akshare_tools.ak') as mock_ak:
            mock_ak.stock_financial_us_report_em.return_value = mock_df

            # Test income statement
            result = QueryUSStockFinacialReport(
                stock="AAPL",
                symbol="综合损益表",
                indicator="年报"
            )

            assert result["symbol"] == "综合损益表"
            assert result["indicator"] == "年报"

            # Test cash flow statement
            mock_ak.stock_financial_us_report_em.return_value = mock_df
            result = QueryUSStockFinacialReport(
                stock="AAPL",
                symbol="现金流量表",
                indicator="单季报"
            )

            assert result["symbol"] == "现金流量表"
            assert result["indicator"] == "单季报"

    def test_query_us_stock_financial_report_empty_response(self):
        """Test QueryUSStockFinacialReport with empty API response."""
        with patch('app.infrastructure.akshare_tools.ak') as mock_ak:
            mock_ak.stock_financial_us_report_em.return_value = pd.DataFrame()

            result = QueryUSStockFinacialReport(
                stock="UNKNOWN",
                symbol="资产负债表",
                indicator="年报"
            )

            assert "error" in result
            assert result["stock"] == "UNKNOWN"
            assert result["symbol"] == "资产负债表"
            assert result["indicator"] == "年报"

    def test_query_us_stock_financial_report_api_error(self):
        """Test QueryUSStockFinacialReport handles API errors."""
        with patch('app.infrastructure.akshare_tools.ak') as mock_ak:
            mock_ak.stock_financial_us_report_em.side_effect = Exception("API Error")

            result = QueryUSStockFinacialReport(
                stock="TSLA",
                symbol="资产负债表",
                indicator="年报"
            )

            assert "error" in result
            assert "API Error" in result["error"]
            assert result["stock"] == "TSLA"

    def test_query_us_stock_financial_report_empty_stock(self):
        """Test QueryUSStockFinacialReport with empty stock code."""
        with pytest.raises(ValueError) as exc_info:
            QueryUSStockFinacialReport(
                stock="",
                symbol="资产负债表",
                indicator="年报"
            )

        assert "股票代码不能为空" in str(exc_info.value)

    def test_query_us_stock_financial_report_invalid_symbol(self):
        """Test QueryUSStockFinacialReport with invalid symbol parameter."""
        with pytest.raises(ValueError) as exc_info:
            QueryUSStockFinacialReport(
                stock="TSLA",
                symbol="无效报表类型",
                indicator="年报"
            )

        assert "报表类型不正确" in str(exc_info.value)

    def test_query_us_stock_financial_report_invalid_indicator(self):
        """Test QueryUSStockFinacialReport with invalid indicator parameter."""
        with pytest.raises(ValueError) as exc_info:
            QueryUSStockFinacialReport(
                stock="TSLA",
                symbol="资产负债表",
                indicator="无效报告期"
            )

        assert "报告期类型不正确" in str(exc_info.value)

    def test_format_financial_report_data(self):
        """Test _format_financial_report_data function."""
        # Create test DataFrame
        test_df = pd.DataFrame({
            'REPORT_DATE': ['2023-12-31', '2023-12-31', '2022-12-31'],
            'ITEM_NAME': ['Total Assets', 'Total Liabilities', 'Total Assets'],
            'AMOUNT': [1000000.0, 500000.0, 800000.0],
            'STD_ITEM_CODE': ['A001', 'L001', 'A001'],
            'REPORT_TYPE': ['Balance Sheet', 'Balance Sheet', 'Balance Sheet'],
            'SECURITY_CODE': ['TSLA', 'TSLA', 'TSLA'],
            'SECURITY_NAME_ABBR': ['Tesla Inc', 'Tesla Inc', 'Tesla Inc']
        })

        result = _format_financial_report_data(
            test_df, "TSLA", "资产负债表", "年报"
        )

        assert result["stock"] == "TSLA"
        assert result["symbol"] == "资产负债表"
        assert result["indicator"] == "年报"
        assert result["total_records"] == 3
        assert len(result["report_dates"]) == 2  # 2023-12-31 and 2022-12-31
        assert "2023-12-31" in result["report_data"]
        assert "2022-12-31" in result["report_data"]
        assert len(result["report_data"]["2023-12-31"]) == 2
        assert len(result["report_data"]["2022-12-31"]) == 1

    def test_format_financial_report_data_empty_dataframe(self):
        """Test _format_financial_report_data with empty DataFrame."""
        empty_df = pd.DataFrame()

        result = _format_financial_report_data(
            empty_df, "TSLA", "资产负债表", "年报"
        )

        assert result["stock"] == "TSLA"
        assert result["symbol"] == "资产负债表"
        assert result["indicator"] == "年报"
        assert result["total_records"] == 0
        assert result["security_code"] is None
        assert result["security_name"] is None
        assert result["report_data"] == {}
        assert result["report_dates"] == []


if __name__ == "__main__":
    pytest.main([__file__])
