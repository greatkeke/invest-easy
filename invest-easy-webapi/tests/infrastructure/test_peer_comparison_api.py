import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.infrastructure.akshare_api.peer_comparison_api import (
    GetStockGrowthComparison,
    GetStockValuationComparison,
    GetStockDupontComparison,
    GetStockScaleComparison,
    GetHKStockGrowthComparison,
    GetHKStockValuationComparison,
    GetHKStockScaleComparison
)


class TestPeerComparisonAPI:
    """Test cases for peer comparison API functions."""

    def test_get_stock_growth_comparison_success(self):
        """Test GetStockGrowthComparison with successful API call."""
        # Create mock DataFrame for growth comparison data
        mock_df = pd.DataFrame({
            '代码': ['行业中值', '行业平均', '000895'],
            '简称': ['行业中值', '行业平均', '双汇发展'],
            '基本每股收益增长率-3年复合': [-8.79, -31.13, 0.84],
            '基本每股收益增长率-24A': [10.5, 15.2, 5.8],
            '基本每股收益增长率-TTM': [12.3, 18.1, 6.2],
            '基本每股收益增长率-25E': [15.0, 20.5, 7.5],
            '基本每股收益增长率-26E': [18.0, 22.8, 8.0],
            '基本每股收益增长率-27E': [20.0, 25.0, 8.5],
            '营业收入增长率-3年复合': [5.5, 8.2, 3.2],
            '营业收入增长率-24A': [6.8, 9.5, 4.1],
            '营业收入增长率-TTM': [7.2, 10.1, 4.5],
            '营业收入增长率-25E': [8.0, 11.5, 5.0],
            '营业收入增长率-26E': [9.0, 12.8, 5.5],
            '营业收入增长率-27E': [10.0, 14.0, 6.0],
            '净利润增长率-3年复合': [8.2, 12.5, 4.3],
            '净利润增长率-24A': [9.5, 14.2, 5.1],
            '净利润增长率-TTM': [10.2, 15.8, 5.8],
            '净利润增长率-25E': [11.0, 17.5, 6.5],
            '净利润增长率-26E': [12.0, 19.2, 7.0],
            '净利润增长率-27E': [13.0, 21.0, 7.5],
            '基本每股收益增长率-3年复合排名': [None, None, 38.0]
        })

        with patch('app.infrastructure.akshare_api.peer_comparison_api.ak') as mock_ak:
            mock_ak.stock_zh_growth_comparison_em.return_value = mock_df

            result = GetStockGrowthComparison(symbol="SZ000895")

            assert result["symbol"] == "SZ000895"
            assert "comparison_data" in result
            assert len(result["comparison_data"]) == 3
            
            # Check specific company data
            target_company = next((item for item in result["comparison_data"] if item["symbol"] == "000895"), None)
            assert target_company is not None
            assert target_company["name"] == "双汇发展"
            assert target_company["eps_growth_3y_compound"] == 0.84
            assert target_company["eps_growth_3y_compound_rank"] == 38.0
            
            # Check units
            assert "units" in result
            assert result["units"]["eps_growth_3y_compound"] == "%"
            assert result["units"]["revenue_growth_3y_compound"] == "%"
            assert result["units"]["net_profit_growth_3y_compound"] == "%"

            mock_ak.stock_zh_growth_comparison_em.assert_called_once_with(
                symbol="SZ000895"
            )

    def test_get_stock_valuation_comparison_success(self):
        """Test GetStockValuationComparison with successful API call."""
        # Create mock DataFrame for valuation comparison data
        mock_df = pd.DataFrame({
            '代码': ['行业平均', '行业中值', '000895'],
            '简称': ['行业平均', '行业中值', '双汇发展'],
            'PEG': [2.48, 0.72, 2.15],
            '市盈率-24A': [25.5, 18.2, 22.8],
            '市盈率-TTM': [26.8, 19.5, 23.5],
            '市盈率-25E': [24.0, 17.0, 21.0],
            '市盈率-26E': [22.5, 16.0, 19.5],
            '市盈率-27E': [21.0, 15.0, 18.0],
            '市销率-24A': [3.2, 2.1, 2.8],
            '市销率-TTM': [3.5, 2.3, 3.0],
            '市销率-25E': [3.0, 2.0, 2.6],
            '市销率-26E': [2.8, 1.8, 2.4],
            '市销率-27E': [2.6, 1.6, 2.2],
            '市净率-24A': [2.5, 1.8, 2.2],
            '市净率-MRQ': [2.6, 1.9, 2.3],
            '市现率PCE-24A': [15.2, 12.5, 14.0],
            '市现率PCE-TTM': [16.0, 13.2, 14.8],
            '市现率PCF-24A': [94.25, -10.07, 63.91],
            '市现率PCF-TTM': [95.0, -9.5, 64.5],
            'EV/EBITDA-24A': [12.79, 18.57, 12.50],
            'PEG排名': [None, None, 58.0]
        })

        with patch('app.infrastructure.akshare_api.peer_comparison_api.ak') as mock_ak:
            mock_ak.stock_zh_valuation_comparison_em.return_value = mock_df

            result = GetStockValuationComparison(symbol="SZ000895")

            assert result["symbol"] == "SZ000895"
            assert "comparison_data" in result
            assert len(result["comparison_data"]) == 3
            
            # Check specific company data
            target_company = next((item for item in result["comparison_data"] if item["symbol"] == "000895"), None)
            assert target_company is not None
            assert target_company["name"] == "双汇发展"
            assert target_company["peg"] == 2.15
            assert target_company["peg_rank"] == 58.0
            assert target_company["pe_24a"] == 22.8
            
            # Check units
            assert "units" in result
            assert result["units"]["peg"] == "倍"
            assert result["units"]["pe_24a"] == "倍"
            assert result["units"]["ps_24a"] == "倍"

            mock_ak.stock_zh_valuation_comparison_em.assert_called_once_with(
                symbol="SZ000895"
            )

    def test_get_stock_dupont_comparison_success(self):
        """Test GetStockDupontComparison with successful API call."""
        # Create mock DataFrame for dupont comparison data
        mock_df = pd.DataFrame({
            '代码': ['行业平均', '行业中值', '000895'],
            '简称': ['行业平均', '行业中值', '双汇发展'],
            'ROE-3年平均': [5.70, 7.71, 24.21],
            'ROE-22A': [5.51, 7.89, 25.17],
            'ROE-23A': [5.85, 8.12, 24.85],
            'ROE-24A': [5.74, 8.32, 24.50],
            '净利率-3年平均': [8.2, 10.5, 15.8],
            '净利率-22A': [8.5, 10.8, 16.2],
            '净利率-23A': [8.1, 10.3, 15.5],
            '净利率-24A': [8.0, 10.4, 15.7],
            '总资产周转率-3年平均': [0.85, 0.92, 1.25],
            '总资产周转率-22A': [0.88, 0.95, 1.28],
            '总资产周转率-23A': [0.82, 0.89, 1.22],
            '总资产周转率-24A': [0.85, 0.92, 1.25],
            '权益乘数-3年平均': [191.76, 149.35, 164.15],
            '权益乘数-22A': [192.50, 150.20, 165.80],
            '权益乘数-23A': [190.80, 148.60, 163.20],
            '权益乘数-24A': [191.00, 149.10, 164.50],
            'ROE-3年平均排名': [None, None, 3.0]
        })

        with patch('app.infrastructure.akshare_api.peer_comparison_api.ak') as mock_ak:
            mock_ak.stock_zh_dupont_comparison_em.return_value = mock_df

            result = GetStockDupontComparison(symbol="SZ000895")

            assert result["symbol"] == "SZ000895"
            assert "comparison_data" in result
            assert len(result["comparison_data"]) == 3
            
            # Check specific company data
            target_company = next((item for item in result["comparison_data"] if item["symbol"] == "000895"), None)
            assert target_company is not None
            assert target_company["name"] == "双汇发展"
            assert target_company["roe_3y_avg"] == 24.21
            assert target_company["roe_3y_avg_rank"] == 3.0
            assert target_company["net_margin_3y_avg"] == 15.8
            
            # Check units
            assert "units" in result
            assert result["units"]["roe_3y_avg"] == "%"
            assert result["units"]["net_margin_3y_avg"] == "%"
            assert result["units"]["asset_turnover_3y_avg"] == "次"

            mock_ak.stock_zh_dupont_comparison_em.assert_called_once_with(
                symbol="SZ000895"
            )

    def test_get_stock_scale_comparison_success(self):
        """Test GetStockScaleComparison with successful API call."""
        # Create mock DataFrame for scale comparison data
        mock_df = pd.DataFrame({
            '代码': ['000895'],
            '简称': ['双汇发展'],
            '总市值': [8.685906e+10],
            '总市值排名': [5],
            '流通市值': [8.6848e+10],
            '流通市值排名': [4],
            '营业收入': [2.850309e+10],
            '营业收入排名': [3],
            '净利润': [2.351218e+09],
            '净利润排名': [3]
        })

        with patch('app.infrastructure.akshare_api.peer_comparison_api.ak') as mock_ak:
            mock_ak.stock_zh_scale_comparison_em.return_value = mock_df

            result = GetStockScaleComparison(symbol="SZ000895")

            assert result["symbol"] == "SZ000895"
            assert "comparison_data" in result
            assert len(result["comparison_data"]) == 1
            
            # Check specific company data
            target_company = result["comparison_data"][0]
            assert target_company["symbol"] == "000895"
            assert target_company["name"] == "双汇发展"
            assert target_company["total_market_cap"] == 8.685906e+10
            assert target_company["total_market_cap_rank"] == 5
            assert target_company["revenue"] == 2.850309e+10
            assert target_company["revenue_rank"] == 3
            
            # Check units
            assert "units" in result
            assert result["units"]["total_market_cap"] == "元"
            assert result["units"]["revenue"] == "元"

            mock_ak.stock_zh_scale_comparison_em.assert_called_once_with(
                symbol="SZ000895"
            )

    def test_get_hk_stock_growth_comparison_success(self):
        """Test GetHKStockGrowthComparison with successful API call."""
        # Create mock DataFrame for HK growth comparison data
        mock_df = pd.DataFrame({
            '代码': ['03900'],
            '简称': ['绿城中国'],
            '基本每股收益同比增长率': [-90.12],
            '基本每股收益同比增长率排名': [171],
            '营业收入同比增长率': [15.8],
            '营业收入同比增长率排名': [45],
            '营业利润率同比增长率': [-25.3],
            '营业利润率同比增长率排名': [120],
            '基本每股收总资产同比增长率益同比增长率': [8.5],
            '总资产同比增长率排名': [91]
        })

        with patch('app.infrastructure.akshare_api.peer_comparison_api.ak') as mock_ak:
            mock_ak.stock_hk_growth_comparison_em.return_value = mock_df

            result = GetHKStockGrowthComparison(symbol="03900")

            assert result["symbol"] == "03900"
            assert "comparison_data" in result
            assert len(result["comparison_data"]) == 1
            
            # Check specific company data
            target_company = result["comparison_data"][0]
            assert target_company["symbol"] == "03900"
            assert target_company["name"] == "绿城中国"
            assert target_company["eps_growth_yoy"] == -90.12
            assert target_company["eps_growth_yoy_rank"] == 171
            assert target_company["revenue_growth_yoy"] == 15.8
            
            # Check units
            assert "units" in result
            assert result["units"]["eps_growth_yoy"] == "%"
            assert result["units"]["revenue_growth_yoy"] == "%"

            mock_ak.stock_hk_growth_comparison_em.assert_called_once_with(
                symbol="03900"
            )

    def test_get_hk_stock_valuation_comparison_success(self):
        """Test GetHKStockValuationComparison with successful API call."""
        # Create mock DataFrame for HK valuation comparison data
        mock_df = pd.DataFrame({
            '代码': ['03900'],
            '简称': ['绿城中国'],
            '市盈率-TTM': [-86.44],
            '市盈率-TTM排名': [97],
            '市盈率-LYR': [14.36],
            '市盈率-LYR排名': [45],
            '市净率-MRQ': [0.85],
            '市净率-MRQ排名': [32],
            '市净率-LYR': [0.92],
            '市净率-LYR排名': [35],
            '市销率-TTM': [1.25],
            '市销率-TTM排名': [28],
            '市销率-LYR': [1.32],
            '市销率-LYR排名': [30],
            '市现率-TTM': [-30.43],
            '市现率-TTM排名': [121],
            '市现率-LYR': [25.68],
            '市现率-LYR排名': [65]
        })

        with patch('app.infrastructure.akshare_api.peer_comparison_api.ak') as mock_ak:
            mock_ak.stock_hk_valuation_comparison_em.return_value = mock_df

            result = GetHKStockValuationComparison(symbol="03900")

            assert result["symbol"] == "03900"
            assert "comparison_data" in result
            assert len(result["comparison_data"]) == 1
            
            # Check specific company data
            target_company = result["comparison_data"][0]
            assert target_company["symbol"] == "03900"
            assert target_company["name"] == "绿城中国"
            assert target_company["pe_ttm"] == -86.44
            assert target_company["pe_ttm_rank"] == 97
            assert target_company["pb_mrq"] == 0.85
            
            # Check units
            assert "units" in result
            assert result["units"]["pe_ttm"] == "倍"
            assert result["units"]["pb_mrq"] == "倍"

            mock_ak.stock_hk_valuation_comparison_em.assert_called_once_with(
                symbol="03900"
            )

    def test_get_hk_stock_scale_comparison_success(self):
        """Test GetHKStockScaleComparison with successful API call."""
        # Create mock DataFrame for HK scale comparison data
        mock_df = pd.DataFrame({
            '代码': ['03900'],
            '简称': ['绿城中国'],
            '总市值': [2.201719e+10],
            '总市值排名': [20],
            '流通市值': [1.850000e+10],
            '流通市值排名': [18],
            '营业总收入': [53368264000],
            '营业总收入排名': [6],
            '净利润': [209907000],
            '净利润排名': [37]
        })

        with patch('app.infrastructure.akshare_api.peer_comparison_api.ak') as mock_ak:
            mock_ak.stock_hk_scale_comparison_em.return_value = mock_df

            result = GetHKStockScaleComparison(symbol="03900")

            assert result["symbol"] == "03900"
            assert "comparison_data" in result
            assert len(result["comparison_data"]) == 1
            
            # Check specific company data
            target_company = result["comparison_data"][0]
            assert target_company["symbol"] == "03900"
            assert target_company["name"] == "绿城中国"
            assert target_company["total_market_cap"] == 2.201719e+10
            assert target_company["total_market_cap_rank"] == 20
            assert target_company["total_revenue"] == 53368264000
            assert target_company["total_revenue_rank"] == 6
            
            # Check units
            assert "units" in result
            assert result["units"]["total_market_cap"] == "港元"
            assert result["units"]["total_revenue"] == "港元"

            mock_ak.stock_hk_scale_comparison_em.assert_called_once_with(
                symbol="03900"
            )

    def test_get_stock_growth_comparison_empty_data(self):
        """Test GetStockGrowthComparison with empty DataFrame."""
        with patch('app.infrastructure.akshare_api.peer_comparison_api.ak') as mock_ak:
            mock_ak.stock_zh_growth_comparison_em.return_value = pd.DataFrame()

            result = GetStockGrowthComparison(symbol="SZ000895")

            assert result["symbol"] == "SZ000895"
            assert "error" in result
            assert "未找到股票" in result["error"]

    def test_get_stock_growth_comparison_api_error(self):
        """Test GetStockGrowthComparison with API error."""
        with patch('app.infrastructure.akshare_api.peer_comparison_api.ak') as mock_ak:
            mock_ak.stock_zh_growth_comparison_em.side_effect = Exception("API Error")

            result = GetStockGrowthComparison(symbol="SZ000895")

            assert result["symbol"] == "SZ000895"
            assert "error" in result
            assert "失败" in result["error"]

    def test_get_stock_growth_comparison_invalid_symbol(self):
        """Test GetStockGrowthComparison with invalid symbol."""
        with pytest.raises(ValueError, match="股票代码不能为空"):
            GetStockGrowthComparison(symbol="")


if __name__ == "__main__":
    pytest.main([__file__])
