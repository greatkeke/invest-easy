import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.infrastructure.akshare_api.stock_finacial_report import (
    GetUSStockFinacialReport,
    GetAStockFinacialReport,
    GetHKStockFinacialReport
)


class TestGetUSStockFinacialReport:
    """Test cases for GetUSStockFinacialReport function."""

    def test_get_us_stock_finacial_report_success(self):
        """Test GetUSStockFinacialReport with successful API call."""
        # Create mock DataFrame for US stock financial report
        mock_df = pd.DataFrame({
            'REPORT_DATE': ['2023-12-31', '2023-09-30'],
            'ITEM_NAME': ['Total Assets', 'Total Liabilities'],
            'AMOUNT': [1000000000.0, 500000000.0],
            'STD_ITEM_CODE': ['ASSETS', 'LIABILITIES'],
            'REPORT_TYPE': ['Balance Sheet', 'Balance Sheet'],
            'SECURITY_CODE': ['TSLA', 'TSLA'],
            'SECURITY_NAME_ABBR': ['Tesla Inc', 'Tesla Inc']
        })

        with patch('app.infrastructure.akshare_api.stock_finacial_report.ak') as mock_ak:
            mock_ak.stock_financial_us_report_em.return_value = mock_df

            result = GetUSStockFinacialReport(
                stock="TSLA",
                symbol="资产负债表",
                indicator="年报"
            )

            assert result["stock"] == "TSLA"
            assert result["symbol"] == "资产负债表"
            assert result["indicator"] == "年报"
            assert result["security_code"] == "TSLA"
            assert result["security_name"] == "Tesla Inc"
            assert result["total_records"] == 2
            assert len(result["report_dates"]) == 2
            assert "2023-12-31" in result["report_data"]
            assert "2023-09-30" in result["report_data"]

            mock_ak.stock_financial_us_report_em.assert_called_once_with(
                stock="TSLA",
                symbol="资产负债表",
                indicator="年报"
            )


class TestGetAStockFinacialReport:
    """Test cases for GetAStockFinacialReport function."""

    def test_get_a_stock_finacial_report_success(self):
        """Test GetAStockFinacialReport with successful API call."""
        # Create mock DataFrames for A stock financial reports
        mock_balance_sheet_df = pd.DataFrame({
            '报告日期': ['2023-12-31'],
            '资产总计': [1000000000.0],
            '负债合计': [500000000.0]
        })

        mock_income_statement_df = pd.DataFrame({
            '报告日期': ['2023-12-31'],
            '营业收入': [800000000.0],
            '净利润': [200000000.0]
        })

        mock_cash_flow_df = pd.DataFrame({
            '报告日期': ['2023-12-31'],
            '经营活动现金流量净额': [150000000.0],
            '投资活动现金流量净额': [-50000000.0]
        })

        with patch('app.infrastructure.akshare_api.stock_finacial_report.ak') as mock_ak:
            mock_ak.stock_financial_debt_ths.return_value = mock_balance_sheet_df
            mock_ak.stock_financial_benefit_ths.return_value = mock_income_statement_df
            mock_ak.stock_financial_cash_ths.return_value = mock_cash_flow_df

            result = GetAStockFinacialReport(
                symbol="000001",
                indicator="按报告期"
            )

            assert result["symbol"] == "000001"
            assert result["indicator"] == "按报告期"
            assert "balance_sheet" in result
            assert "income_statement" in result
            assert "cash_flow" in result
            assert result["balance_sheet"]["total_records"] == 1
            assert result["income_statement"]["total_records"] == 1
            assert result["cash_flow"]["total_records"] == 1

            mock_ak.stock_financial_debt_ths.assert_called_once_with(
                symbol="000001",
                indicator="按报告期"
            )
            mock_ak.stock_financial_benefit_ths.assert_called_once_with(
                symbol="000001",
                indicator="按报告期"
            )
            mock_ak.stock_financial_cash_ths.assert_called_once_with(
                symbol="000001",
                indicator="按报告期"
            )


class TestGetHKStockFinacialReport:
    """Test cases for GetHKStockFinacialReport function."""

    def test_get_hk_stock_finacial_report_success(self):
        """Test GetHKStockFinacialReport with successful API call."""
        # Create mock DataFrame for HK stock financial report
        mock_df = pd.DataFrame({
            'REPORT_DATE': ['2023-12-31', '2023-06-30'],
            'STD_ITEM_NAME': ['Total Assets', 'Total Liabilities'],
            'AMOUNT': [500000000.0, 250000000.0],
            'STD_ITEM_CODE': ['ASSETS', 'LIABILITIES'],
            'FISCAL_YEAR': [2023, 2023],
            'DATE_TYPE_CODE': ['A', 'A'],
            'SECUCODE': ['00700', '00700'],
            'SECURITY_CODE': ['00700', '00700'],
            'SECURITY_NAME_ABBR': ['Tencent Holdings', 'Tencent Holdings'],
            'ORG_CODE': ['12345', '12345']
        })

        with patch('app.infrastructure.akshare_api.stock_finacial_report.ak') as mock_ak:
            mock_ak.stock_financial_hk_report_em.return_value = mock_df

            result = GetHKStockFinacialReport(
                stock="00700",
                symbol="资产负债表",
                indicator="年度"
            )

            assert result["stock"] == "00700"
            assert result["symbol"] == "资产负债表"
            assert result["indicator"] == "年度"
            assert result["security_code"] == "00700"
            assert result["security_name"] == "Tencent Holdings"
            assert result["total_records"] == 2
            assert len(result["report_dates"]) == 2
            assert "2023-12-31" in result["report_data"]
            assert "2023-06-30" in result["report_data"]

            mock_ak.stock_financial_hk_report_em.assert_called_once_with(
                stock="00700",
                symbol="资产负债表",
                indicator="年度"
            )


if __name__ == "__main__":
    pytest.main([__file__])
