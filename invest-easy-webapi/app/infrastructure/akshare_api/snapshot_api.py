import logging
from typing import Dict, Any
import akshare as ak
from pandas import DataFrame

def GetStockSpotData(symbol: str) -> Dict[str, Any]:
    """
    获取指定股票最新的行情数据（雪球接口）

    Args:
        symbol: 证券代码，可以是 A 股个股代码，A 股场内基金代码，A 股指数，美股代码, 美股指数，港股股票
               例如 "SH600000", "SZ000001", "USTSLA", "HK00700"

    Returns:
        Dict[str, Any]: 包含最新行情数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        logging.info(f"正在查询股票 {symbol} 的最新行情数据...")

        # 调用akshare的stock_individual_spot_xq接口
        stock_spot_df = ak.stock_individual_spot_xq(symbol=symbol)

        if isinstance(stock_spot_df, DataFrame) and not stock_spot_df.empty:
            # 格式化行情数据
            result = _format_stock_spot_data(stock_spot_df, symbol)
            logging.info(f"成功获取股票 {symbol} 的最新行情数据")
            return result
        else:
            error_msg = f"未找到股票 {symbol} 的行情数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}

    except Exception as e:
        error_msg = f"获取股票 {symbol} 行情数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def _format_stock_spot_data(raw_df: DataFrame, symbol: str) -> Dict[str, Any]:
    """
    格式化股票行情数据，将中文字段名转换为英文，并处理特殊值

    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码

    Returns:
        Dict[str, Any]: 格式化后的行情数据
    """
    # 转换为字典列表
    records = raw_df.to_dict("records")

    if not records:
        return {"error": "未找到行情数据", "symbol": symbol}

    # 中文到英文字段名映射
    field_mapping = {
        "代码": "symbol",
        "52周最高": "week_52_high",
        "流通股": "circulating_shares",
        "跌停": "limit_down",
        "最高": "high",
        "流通值": "circulating_market_cap",
        "最小交易单位": "min_trade_unit",
        "涨跌": "change_amount",
        "每股收益": "eps",
        "昨收": "previous_close",
        "成交量": "volume",
        "周转率": "turnover_rate",
        "52周最低": "week_52_low",
        "名称": "name",
        "交易所": "exchange",
        "市盈率(动)": "pe_dynamic",
        "基金份额/总股本": "total_shares",
        "净资产中的商誉": "goodwill_in_net_assets",
        "均价": "average_price",
        "涨幅": "change_percent",
        "振幅": "amplitude",
        "现价": "current_price",
        "今年以来涨幅": "ytd_change_percent",
        "发行日期": "issue_date",
        "最低": "low",
        "资产净值/总市值": "nav_to_market_cap",
        "股息(TTM)": "dividend_ttm",
        "股息率(TTM)": "dividend_yield_ttm",
        "货币": "currency",
        "每股净资产": "nav_per_share",
        "市盈率(静)": "pe_static",
        "成交额": "turnover",
        "市净率": "pb_ratio",
        "涨停": "limit_up",
        "市盈率(TTM)": "pe_ttm",
        "时间": "timestamp",
        "今开": "open",
    }

    # 构建结果
    result: Dict[str, Any] = {"symbol": symbol}

    for record in records:
        chinese_item = record.get("item")
        value = record.get("value")

        # 处理特殊值（NaN等）
        if isinstance(value, float) and (value != value):  # 检查NaN
            value = None

        # 映射字段名 - 确保chinese_item是字符串
        if isinstance(chinese_item, str):
            english_field = field_mapping.get(chinese_item)
            if english_field:
                result[english_field] = value

    # 添加单位说明
    result["units"] = {
        "week_52_high": "元",
        "circulating_shares": "股",
        "limit_down": "元",
        "high": "元",
        "circulating_market_cap": "元",
        "min_trade_unit": "股",
        "change_amount": "元",
        "eps": "元",
        "previous_close": "元",
        "volume": "股",
        "turnover_rate": "%",
        "week_52_low": "元",
        "pe_dynamic": "倍",
        "total_shares": "股",
        "goodwill_in_net_assets": "元",
        "average_price": "元",
        "change_percent": "%",
        "amplitude": "%",
        "current_price": "元",
        "ytd_change_percent": "%",
        "low": "元",
        "nav_to_market_cap": "倍",
        "dividend_ttm": "元",
        "dividend_yield_ttm": "%",
        "nav_per_share": "元",
        "pe_static": "倍",
        "turnover": "元",
        "pb_ratio": "倍",
        "limit_up": "元",
        "pe_ttm": "倍",
        "open": "元",
    }

    return result
