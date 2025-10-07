import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.infrastructure.akshare_api.stock_news_api import GetStockNews


class TestGetStockNews:
    """Test cases for GetStockNews function."""

    def test_get_stock_news_success(self):
        """Test GetStockNews with successful API call."""
        # Create mock DataFrame for stock news data
        mock_df = pd.DataFrame({
            '关键词': ['603777', '603777', '603777'],
            '新闻标题': [
                '来伊份发布2024年第一季度财报',
                '来伊份与京东达成战略合作',
                '来伊份股价创年内新高'
            ],
            '新闻内容': [
                '来伊份(603777)发布2024年第一季度财报，营收同比增长15%...',
                '来伊份与京东达成战略合作，将在供应链、物流等方面深度合作...',
                '来伊份股价今日上涨5%，创年内新高，市值突破100亿元...'
            ],
            '发布时间': [
                '2024-04-30 09:00:00',
                '2024-04-28 14:30:00',
                '2024-04-25 16:45:00'
            ],
            '文章来源': [
                '东方财富网',
                '证券时报',
                '中国证券报'
            ],
            '新闻链接': [
                'http://finance.eastmoney.com/a/20240430123456789.html',
                'http://finance.eastmoney.com/a/20240428123456789.html',
                'http://finance.eastmoney.com/a/20240425123456789.html'
            ]
        })

        with patch('app.infrastructure.akshare_api.stock_news_api.ak') as mock_ak:
            mock_ak.stock_news_em.return_value = mock_df

            result = GetStockNews(symbol="603777")

            # Check basic structure
            assert result["symbol"] == "603777"
            assert result["total_count"] == 3
            assert "news" in result
            assert len(result["news"]) == 3

            # Check first news item
            first_news = result["news"][0]
            assert first_news["keywords"] == "603777"
            assert first_news["title"] == "来伊份发布2024年第一季度财报"
            assert first_news["content"] == "来伊份(603777)发布2024年第一季度财报，营收同比增长15%..."
            assert first_news["publish_time"] == "2024-04-30 09:00:00"
            assert first_news["source"] == "东方财富网"
            assert first_news["url"] == "http://finance.eastmoney.com/a/20240430123456789.html"

            # Check second news item
            second_news = result["news"][1]
            assert second_news["keywords"] == "603777"
            assert second_news["title"] == "来伊份与京东达成战略合作"
            assert second_news["source"] == "证券时报"

            # Check third news item
            third_news = result["news"][2]
            assert third_news["keywords"] == "603777"
            assert third_news["title"] == "来伊份股价创年内新高"
            assert third_news["source"] == "中国证券报"

            mock_ak.stock_news_em.assert_called_once_with(
                symbol="603777"
            )

    def test_get_stock_news_empty_result(self):
        """Test GetStockNews with empty result."""
        # Create empty DataFrame
        mock_df = pd.DataFrame()

        with patch('app.infrastructure.akshare_api.stock_news_api.ak') as mock_ak:
            mock_ak.stock_news_em.return_value = mock_df

            result = GetStockNews(symbol="603777")

            assert "error" in result
            assert result["symbol"] == "603777"
            assert "未找到股票" in result["error"]

            mock_ak.stock_news_em.assert_called_once_with(
                symbol="603777"
            )

    def test_get_stock_news_api_error(self):
        """Test GetStockNews with API error."""
        with patch('app.infrastructure.akshare_api.stock_news_api.ak') as mock_ak:
            mock_ak.stock_news_em.side_effect = Exception("API connection failed")

            result = GetStockNews(symbol="603777")

            assert "error" in result
            assert result["symbol"] == "603777"
            assert "获取股票" in result["error"]
            assert "API connection failed" in result["error"]

            mock_ak.stock_news_em.assert_called_once_with(
                symbol="603777"
            )

    def test_get_stock_news_empty_symbol(self):
        """Test GetStockNews with empty symbol."""
        with pytest.raises(ValueError, match="股票代码不能为空"):
            GetStockNews(symbol="")


if __name__ == "__main__":
    pytest.main([__file__])
