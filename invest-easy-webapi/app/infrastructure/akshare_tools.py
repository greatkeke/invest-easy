import logging
import json
from datetime import date, datetime
from typing import Dict, Any
from langchain_core.tools import tool
from .akshare_api.historical_data_api import GetStockHistoricalData
from .akshare_api.stock_value_api import GetStockValue
from .akshare_api.stock_finacial_report import (
    GetAStockFinacialReport,
    GetHKStockFinacialReport,
    GetUSStockFinacialReport,
)
from .akshare_api.snapshot_api import GetStockSpotData
from .akshare_api.stock_news_api import GetStockNews
from .easy_tools import read_file, write_file


class DateTimeEncoder(json.JSONEncoder):
    """自定义JSON编码器，处理datetime和date对象"""
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return super().default(o)

@tool
def QueryStockHistoricalData(
    symbol: str, start_date: str, end_date: str, adjust: str = "", period: str = "auto"
) -> Dict[str, Any]:
    """
    获取股票历史行情数据

    根据时间跨度自动选择数据频率：
    - 默认获取daily数据
    - 时间跨度大于一个月的获取weekly数据
    - 时间跨度大于一年的获取monthly数据

    Args:
        symbol: 股票代码
            - A股: 6位数字代码，如 "000001"
            - 美股: 字母代码，如 "AAPL"
            - 港股: 5位数字代码，如 "00700"
        start_date: 开始日期，格式为 "YYYYMMDD"，如 "20230101"
        end_date: 结束日期，格式为 "YYYYMMDD"，如 "20231231"
        adjust: 复权类型，可选值: {"", "qfq", "hfq"}，默认为 "" (不复权)
        period: 数据频率，可选值: {"auto", "daily", "weekly", "monthly"}，默认为 "auto" (自动选择)

    Returns:
        Dict[str, Any]: 包含历史行情数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当参数为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    # 生成缓存key，包含所有参数
    cache_key = f"{symbol}_{start_date}_{end_date}_{adjust}_{period}"
    
    # 先尝试从缓存读取
    cached_data = read_file("QueryStockHistoricalData", cache_key)
    if cached_data:
        logging.info(f"从缓存读取股票 {symbol} 历史行情数据")
        return json.loads(cached_data)
    
    # 缓存不存在，调用API获取数据
    logging.info(f"调用API获取股票 {symbol} 历史行情数据")
    result = GetStockHistoricalData(symbol, start_date, end_date, adjust, period)
    
    # 将结果写入缓存
    if result and "error" not in result:
        write_file("QueryStockHistoricalData", cache_key, json.dumps(result, ensure_ascii=False, cls=DateTimeEncoder))
        logging.info(f"已将股票 {symbol} 历史行情数据写入缓存")
    
    return result


@tool
def QueryStockValue(symbol: str) -> Dict[str, Any]:
    """
    执行个股估值查询，仅支持A股。

    Args:
        symbol: A股代码，例如 "002044" 或 "300766"

    Returns:
        Dict[str, Any]: 包含估值数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    # 先尝试从缓存读取
    cached_data = read_file("QueryStockValue", symbol)
    if cached_data:
        logging.info(f"从缓存读取股票 {symbol} 估值数据")
        return json.loads(cached_data)
    
    # 缓存不存在，调用API获取数据
    logging.info(f"调用API获取股票 {symbol} 估值数据")
    result = GetStockValue(symbol)
    
    # 将结果写入缓存
    if result and "error" not in result:
        write_file("QueryStockValue", symbol, json.dumps(result, ensure_ascii=False, cls=DateTimeEncoder))
        logging.info(f"已将股票 {symbol} 估值数据写入缓存")
    
    return result


@tool
def QueryStockFinacialReport(
    stock: str, symbol: str = "资产负债表", indicator: str = "年报"
) -> Dict[str, Any]:
    """
    查询股票财务报表数据
    
    根据股票代码自动识别市场类型并调用相应的财务报表接口：
    - A股: 6位数字代码，如 "000001"
    - 港股: 5位数字代码，如 "00700"  
    - 美股: 字母代码，如 "AAPL" 或 "BRK_A"（注意：BRK.A 需要转换为 BRK_A）

    Args:
        stock: 股票代码
            - A股: 6位数字代码，如 "000001"
            - 港股: 5位数字代码，如 "00700"
            - 美股: 字母代码，如 "AAPL" 或 "BRK_A"
        symbol: 报表类型
            - A股: 可选值: {"按报告期", "按年度", "按单季度"}，默认为 "按报告期"
            - 港股: 可选值: {"资产负债表", "利润表", "现金流量表"}，默认为 "资产负债表"
            - 美股: 可选值: {"资产负债表", "综合损益表", "现金流量表"}，默认为 "资产负债表"
        indicator: 报告期类型
            - A股: 可选值: {"按报告期", "按年度", "按单季度"}，默认为 "按报告期"
            - 港股: 可选值: {"年度", "报告期"}，默认为 "年度"
            - 美股: 可选值: {"年报", "单季报", "累计季报"}，默认为 "年报"

    Returns:
        Dict[str, Any]: 包含财务报表数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当参数为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    if not stock:
        raise ValueError("股票代码不能为空")

    try:
        # 生成缓存key，包含所有参数
        cache_key = f"{stock}_{symbol}_{indicator}"
        
        # 先尝试从缓存读取
        cached_data = read_file("QueryStockFinacialReport", cache_key)
        if cached_data:
            logging.info(f"从缓存读取股票 {stock} 财务报表数据")
            return json.loads(cached_data)
        
        logging.info(f"正在查询股票 {stock} 的财务报表数据，报表类型: {symbol}，报告期: {indicator}")

        # 根据股票代码格式判断市场类型
        if stock.isdigit():
            if len(stock) == 6:
                # A股 - 6位数字代码
                logging.info(f"识别为A股代码: {stock}")
                # A股的参数映射：symbol参数是股票代码，indicator参数是报告期类型
                # 对于A股，symbol参数需要调整为indicator，indicator参数需要调整为A股的有效值
                a_stock_indicator = "按报告期"  # A股的默认报告期类型
                if indicator == "年报":
                    a_stock_indicator = "按年度"
                elif indicator == "单季报":
                    a_stock_indicator = "按单季度"
                # 如果indicator已经是A股的有效值，则直接使用
                elif indicator in {"按报告期", "按年度", "按单季度"}:
                    a_stock_indicator = indicator
                
                result = GetAStockFinacialReport(symbol=stock, indicator=a_stock_indicator)
            elif len(stock) == 5:
                # 港股 - 5位数字代码
                logging.info(f"识别为港股代码: {stock}")
                # 港股的参数映射：indicator参数需要调整为港股的有效值
                hk_indicator = "年度"  # 港股的默认报告期类型
                if indicator == "年报":
                    hk_indicator = "年度"
                elif indicator == "单季报":
                    hk_indicator = "报告期"
                # 如果indicator已经是港股的有效值，则直接使用
                elif indicator in {"年度", "报告期"}:
                    hk_indicator = indicator
                
                result = GetHKStockFinacialReport(stock=stock, symbol=symbol, indicator=hk_indicator)
            else:
                error_msg = f"无法识别的股票代码格式: {stock}，应为6位数字(A股)或5位数字(港股)"
                logging.error(error_msg)
                result = {"error": error_msg, "stock": stock}
        else:
            # 美股 - 字母代码
            logging.info(f"识别为美股代码: {stock}")
            # 美股的参数直接使用，因为默认值已经匹配
            result = GetUSStockFinacialReport(stock=stock, symbol=symbol, indicator=indicator)

        # 将结果写入缓存
        if result and "error" not in result:
            write_file("QueryStockFinacialReport", cache_key, json.dumps(result, ensure_ascii=False, cls=DateTimeEncoder))
            logging.info(f"已将股票 {stock} 财务报表数据写入缓存")
        
        return result

    except Exception as e:
        error_msg = f"查询股票 {stock} 财务报表数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "stock": stock, "symbol": symbol, "indicator": indicator}


@tool
def QueryStockSpotData(symbol: str) -> Dict[str, Any]:
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
    # 先尝试从缓存读取
    cached_data = read_file("QueryStockSpotData", symbol)
    if cached_data:
        logging.info(f"从缓存读取股票 {symbol} 实时行情数据")
        return json.loads(cached_data)
    
    # 缓存不存在，调用API获取数据
    logging.info(f"调用API获取股票 {symbol} 实时行情数据")
    result = GetStockSpotData(symbol)
    
    # 将结果写入缓存
    if result and "error" not in result:
        write_file("QueryStockSpotData", symbol, json.dumps(result, ensure_ascii=False, cls=DateTimeEncoder))
        logging.info(f"已将股票 {symbol} 实时行情数据写入缓存")
    
    return result


@tool
def QueryStockPeerComparison(symbol: str) -> Dict[str, Any]:
    """
    获取股票同行比较数据

    根据股票代码自动识别市场类型并调用相应的同行比较接口：
    - A股: 6位数字代码，如 "000001" 或带交易所前缀如 "SZ000001"
    - 港股: 5位数字代码，如 "00700" 或带交易所前缀如 "HK00700"

    返回包含成长性、估值、杜邦分析和公司规模四个维度的同行比较数据。

    Args:
        symbol: 股票代码
            - A股: 6位数字代码，如 "000001" 或带交易所前缀如 "SZ000001"
            - 港股: 5位数字代码，如 "00700" 或带交易所前缀如 "HK00700"

    Returns:
        Dict[str, Any]: 包含同行比较数据的字典，结构如下：
            {
                "symbol": "股票代码",
                "market": "市场类型(A股/港股)",
                "growth_comparison": {...},  # 成长性比较数据
                "valuation_comparison": {...},  # 估值比较数据
                "dupont_comparison": {...},  # 杜邦分析比较数据
                "scale_comparison": {...},  # 公司规模比较数据
                "units": {...}  # 数据单位说明
            }
            如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        # 先尝试从缓存读取
        cached_data = read_file("QueryStockPeerComparison", symbol)
        if cached_data:
            logging.info(f"从缓存读取股票 {symbol} 同行比较数据")
            return json.loads(cached_data)
        
        logging.info(f"正在查询股票 {symbol} 的同行比较数据")

        # 标准化symbol格式，移除交易所前缀
        clean_symbol = symbol.upper()
        if clean_symbol.startswith("SZ") or clean_symbol.startswith("SH"):
            # A股带交易所前缀，提取纯数字代码
            clean_symbol = clean_symbol[2:]
        elif clean_symbol.startswith("HK"):
            # 港股带交易所前缀，提取纯数字代码
            clean_symbol = clean_symbol[2:]

        # 根据股票代码格式判断市场类型
        if clean_symbol.isdigit():
            if len(clean_symbol) == 6:
                # A股 - 6位数字代码
                logging.info(f"识别为A股代码: {clean_symbol}")
                result = _get_a_stock_peer_comparison(clean_symbol)
            elif len(clean_symbol) == 5:
                # 港股 - 5位数字代码
                logging.info(f"识别为港股代码: {clean_symbol}")
                result = _get_hk_stock_peer_comparison(clean_symbol)
            else:
                error_msg = f"无法识别的股票代码格式: {symbol}，应为6位数字(A股)或5位数字(港股)"
                logging.error(error_msg)
                result = {"error": error_msg, "symbol": symbol}
        else:
            error_msg = f"无法识别的股票代码格式: {symbol}，应为数字代码"
            logging.error(error_msg)
            result = {"error": error_msg, "symbol": symbol}

        # 将结果写入缓存
        if result and "error" not in result:
            write_file("QueryStockPeerComparison", symbol, json.dumps(result, ensure_ascii=False, cls=DateTimeEncoder))
            logging.info(f"已将股票 {symbol} 同行比较数据写入缓存")
        
        return result

    except Exception as e:
        error_msg = f"查询股票 {symbol} 同行比较数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def _get_a_stock_peer_comparison(symbol: str) -> Dict[str, Any]:
    """
    获取A股股票同行比较数据

    Args:
        symbol: A股股票代码，6位数字

    Returns:
        Dict[str, Any]: 包含A股同行比较数据的字典
    """
    from .akshare_api.peer_comparison_api import (
        GetStockGrowthComparison,
        GetStockValuationComparison,
        GetStockDupontComparison,
        GetStockScaleComparison
    )

    result = {
        "symbol": symbol,
        "market": "A股",
        "growth_comparison": GetStockGrowthComparison(symbol),
        "valuation_comparison": GetStockValuationComparison(symbol),
        "dupont_comparison": GetStockDupontComparison(symbol),
        "scale_comparison": GetStockScaleComparison(symbol)
    }

    # 合并单位说明
    result["units"] = {
        "growth_comparison": result["growth_comparison"].get("units", {}),
        "valuation_comparison": result["valuation_comparison"].get("units", {}),
        "dupont_comparison": result["dupont_comparison"].get("units", {}),
        "scale_comparison": result["scale_comparison"].get("units", {})
    }

    return result


def _get_hk_stock_peer_comparison(symbol: str) -> Dict[str, Any]:
    """
    获取港股股票同行比较数据

    Args:
        symbol: 港股股票代码，5位数字

    Returns:
        Dict[str, Any]: 包含港股同行比较数据的字典
    """
    from .akshare_api.peer_comparison_api import (
        GetHKStockGrowthComparison,
        GetHKStockValuationComparison,
        GetHKStockScaleComparison
    )

    result = {
        "symbol": symbol,
        "market": "港股",
        "growth_comparison": GetHKStockGrowthComparison(symbol),
        "valuation_comparison": GetHKStockValuationComparison(symbol),
        "scale_comparison": GetHKStockScaleComparison(symbol)
    }

    # 港股没有杜邦分析比较数据
    result["dupont_comparison"] = {
        "error": "港股暂不支持杜邦分析比较数据",
        "symbol": symbol
    }

    # 合并单位说明
    result["units"] = {
        "growth_comparison": result["growth_comparison"].get("units", {}),
        "valuation_comparison": result["valuation_comparison"].get("units", {}),
        "scale_comparison": result["scale_comparison"].get("units", {})
    }

    return result

@tool
def QueryStockNews(symbol: str) -> Dict[str, Any]:
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
    # 先尝试从缓存读取
    cached_data = read_file("QueryStockNews", symbol)
    if cached_data:
        logging.info(f"从缓存读取股票 {symbol} 新闻数据")
        return json.loads(cached_data)
    
    # 缓存不存在，调用API获取数据
    logging.info(f"调用API获取股票 {symbol} 新闻数据")
    result = GetStockNews(symbol)
    
    # 将结果写入缓存
    if result and "error" not in result:
        write_file("QueryStockNews", symbol, json.dumps(result, ensure_ascii=False, cls=DateTimeEncoder))
        logging.info(f"已将股票 {symbol} 新闻数据写入缓存")
    
    return result
