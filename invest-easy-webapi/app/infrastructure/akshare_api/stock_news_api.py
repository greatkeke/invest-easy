import logging
from typing import Dict, Any, List
import akshare as ak
from pandas import DataFrame

def GetStockNews(symbol: str) -> Dict[str, Any]:
    """
    获取指定股票的最新新闻资讯数据（东方财富接口）

    Args:
        symbol: 股票代码，例如 "603777"

    Returns:
        Dict[str, Any]: 包含新闻数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        logging.info(f"正在查询股票 {symbol} 的最新新闻资讯...")

        # 调用akshare的stock_news_em接口
        stock_news_df = ak.stock_news_em(symbol=symbol)

        if isinstance(stock_news_df, DataFrame) and not stock_news_df.empty:
            # 格式化新闻数据
            result = _format_stock_news_data(stock_news_df, symbol)
            logging.info(f"成功获取股票 {symbol} 的新闻资讯数据，共 {len(result['news'])} 条")
            return result
        else:
            error_msg = f"未找到股票 {symbol} 的新闻资讯数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}

    except Exception as e:
        error_msg = f"获取股票 {symbol} 新闻资讯数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def _format_stock_news_data(raw_df: DataFrame, symbol: str) -> Dict[str, Any]:
    """
    格式化股票新闻数据，将中文字段名转换为英文，并处理数据格式

    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码

    Returns:
        Dict[str, Any]: 格式化后的新闻数据
    """
    # 转换为字典列表
    records = raw_df.to_dict("records")

    if not records:
        return {"error": "未找到新闻数据", "symbol": symbol}

    # 中文到英文字段名映射
    field_mapping = {
        "关键词": "keywords",
        "新闻标题": "title",
        "新闻内容": "content",
        "发布时间": "publish_time",
        "文章来源": "source",
        "新闻链接": "url"
    }

    # 构建新闻列表
    news_list: List[Dict[str, Any]] = []

    for record in records:
        news_item: Dict[str, Any] = {}
        
        for chinese_field, english_field in field_mapping.items():
            value = record.get(chinese_field)
            
            # 处理特殊值（NaN等）
            if isinstance(value, float) and (value != value):  # 检查NaN
                value = None
            elif value is None:
                value = ""
            
            news_item[english_field] = value
        
        # 添加到新闻列表
        news_list.append(news_item)

    # 构建结果
    result: Dict[str, Any] = {
        "symbol": symbol,
        "news": news_list,
        "total_count": len(news_list)
    }

    return result
