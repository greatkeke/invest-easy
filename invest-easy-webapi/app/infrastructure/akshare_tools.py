import logging
from typing import Dict, Any, Optional, Union, List
import akshare as ak
from pandas import DataFrame
from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field
from akshare_api.historical_data_api import GetStockHistoricalData

@tool
def QueryStockHistoricalData(
    symbol: str,
    start_date: str,
    end_date: str,
    adjust: str = "",
    period: str = "auto"
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
    return GetStockHistoricalData(symbol, start_date, end_date, adjust, period)


@tool
def QueryStockValue(symbol: str) -> Dict[str, Any]:
    """
    执行个股估值查询
    
    Args:
        symbol: A股代码，例如 "002044" 或 "300766"
        
    Returns:
        Dict[str, Any]: 包含估值数据的字典，如果查询失败则返回错误信息
        
    Raises:
        ValueError: 当symbol为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")
    
    # 验证A股代码格式（6位数字）
    if not symbol.isdigit() or len(symbol) != 6:
        raise ValueError(f"股票代码格式不正确: {symbol}，应为6位数字")
    
    try:
        logging.info(f"正在查询股票 {symbol} 的估值数据...")
        
        # 调用akshare的stock_value_em接口
        stock_value_em_df = ak.stock_value_em(symbol=symbol)
        
        if isinstance(stock_value_em_df, DataFrame) and not stock_value_em_df.empty:
            # 获取最新数据（最后一行）
            latest_data = stock_value_em_df.iloc[-1].to_dict()
            
            # 转换字段名为英文并处理数据
            result = _format_valuation_data(latest_data, symbol)
            logging.info(f"成功获取股票 {symbol} 的估值数据")
            return result
        else:
            error_msg = f"未找到股票 {symbol} 的估值数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}
            
    except Exception as e:
        error_msg = f"获取股票 {symbol} 估值数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}

def _format_valuation_data(raw_data: Dict[str, Any], symbol: str) -> Dict[str, Any]:
    """
    格式化估值数据，将中文字段名转换为英文，并处理特殊值
    
    Args:
        raw_data: 原始数据字典
        symbol: 股票代码
        
    Returns:
        Dict[str, Any]: 格式化后的估值数据
    """
    # 中文到英文字段名映射
    field_mapping = {
        "数据日期": "date",
        "当日收盘价": "close_price",
        "当日涨跌幅": "change_percent",
        "总市值": "total_market_cap",
        "流通市值": "circulating_market_cap",
        "总股本": "total_shares",
        "流通股本": "circulating_shares",
        "PE(TTM)": "pe_ttm",
        "PE(静)": "pe_static",
        "市净率": "pb_ratio",
        "PEG值": "peg_ratio",
        "市现率": "pcf_ratio",
        "市销率": "ps_ratio"
    }
    
    # 格式化数据
    formatted_data: Dict[str, Any] = {"symbol": symbol}
    
    for chinese_field, english_field in field_mapping.items():
        value = raw_data.get(chinese_field)
        
        # 处理特殊值（NaN等）
        if isinstance(value, float) and (value != value):  # 检查NaN
            formatted_data[english_field] = None
        else:
            formatted_data[english_field] = value
    
    # 添加单位说明
    formatted_data["units"] = {
        "close_price": "元",
        "change_percent": "%",
        "total_market_cap": "元",
        "circulating_market_cap": "元",
        "total_shares": "股",
        "circulating_shares": "股",
        "pe_ttm": "倍",
        "pe_static": "倍",
        "pb_ratio": "倍",
        "peg_ratio": "倍",
        "pcf_ratio": "倍",
        "ps_ratio": "倍"
    }
    
    return formatted_data


@tool
def QueryUSStockFinacialReport(
    stock: str, 
    symbol: str = "资产负债表", 
    indicator: str = "年报"
) -> Dict[str, Any]:
    """
    查询美股财务报表数据
    
    Args:
        stock: 美股代码，例如 "TSLA" 或 "BRK_A"（注意：BRK.A 需要转换为 BRK_A）
        symbol: 报表类型，可选值: {"资产负债表", "综合损益表", "现金流量表"}，默认为 "资产负债表"
        indicator: 报告期类型，可选值: {"年报", "单季报", "累计季报"}，默认为 "年报"
        
    Returns:
        Dict[str, Any]: 包含财务报表数据的字典，如果查询失败则返回错误信息
        
    Raises:
        ValueError: 当参数为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    if not stock:
        raise ValueError("股票代码不能为空")
    
    # 验证报表类型参数
    valid_symbols = {"资产负债表", "综合损益表", "现金流量表"}
    if symbol not in valid_symbols:
        raise ValueError(f"报表类型不正确: {symbol}，应为 {valid_symbols}")
    
    # 验证报告期类型参数
    valid_indicators = {"年报", "单季报", "累计季报"}
    if indicator not in valid_indicators:
        raise ValueError(f"报告期类型不正确: {indicator}，应为 {valid_indicators}")
    
    try:
        # 处理股票代码格式（如果包含点号，转换为下划线）
        processed_stock = stock.replace('.', '_')
        
        logging.info(f"正在查询美股 {stock} 的财务报表数据，报表类型: {symbol}，报告期: {indicator}")
        
        # 调用akshare的stock_financial_us_report_em接口
        financial_report_df = ak.stock_financial_us_report_em(
            stock=processed_stock,
            symbol=symbol,
            indicator=indicator
        )
        
        if isinstance(financial_report_df, DataFrame) and not financial_report_df.empty:
            # 格式化财务报表数据
            result = _format_financial_report_data(financial_report_df, stock, symbol, indicator)
            logging.info(f"成功获取美股 {stock} 的财务报表数据，共 {len(financial_report_df)} 条记录")
            return result
        else:
            error_msg = f"未找到美股 {stock} 的财务报表数据"
            logging.warning(error_msg)
            return {"error": error_msg, "stock": stock, "symbol": symbol, "indicator": indicator}
            
    except Exception as e:
        error_msg = f"获取美股 {stock} 财务报表数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "stock": stock, "symbol": symbol, "indicator": indicator}


def _format_financial_report_data(
    raw_df: DataFrame, 
    stock: str, 
    symbol: str, 
    indicator: str
) -> Dict[str, Any]:
    """
    格式化财务报表数据，转换为更易读的结构
    
    Args:
        raw_df: 原始DataFrame数据
        stock: 股票代码
        symbol: 报表类型
        indicator: 报告期类型
        
    Returns:
        Dict[str, Any]: 格式化后的财务报表数据
    """
    # 转换为字典列表
    records = raw_df.to_dict('records')
    
    # 按报告日期分组数据
    grouped_data = {}
    for record in records:
        report_date = record.get('REPORT_DATE')
        if report_date not in grouped_data:
            grouped_data[report_date] = []
        
        # 处理每个项目的数据
        item_data = {
            "item_name": record.get('ITEM_NAME'),
            "amount": record.get('AMOUNT'),
            "std_item_code": record.get('STD_ITEM_CODE'),
            "report_type": record.get('REPORT_TYPE')
        }
        grouped_data[report_date].append(item_data)
    
    # 构建结果
    result = {
        "stock": stock,
        "symbol": symbol,
        "indicator": indicator,
        "security_code": records[0].get('SECURITY_CODE') if records else None,
        "security_name": records[0].get('SECURITY_NAME_ABBR') if records else None,
        "report_data": grouped_data,
        "total_records": len(records),
        "report_dates": list(grouped_data.keys())
    }
    
    return result


@tool
def QueryAStockFinacialReport(
    symbol: str, 
    indicator: str = "按报告期"
) -> Dict[str, Any]:
    """
    查询A股财务报表数据（同花顺）
    
    Args:
        symbol: A股代码，例如 "000063" (中兴通讯)
        indicator: 报告期类型，可选值: {"按报告期", "按年度", "按单季度"}，默认为 "按报告期"
        
    Returns:
        Dict[str, Any]: 包含财务报表数据的字典，包含资产负债表、利润表、现金流量表数据
        
    Raises:
        ValueError: 当参数为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")
    
    # 验证A股代码格式（6位数字）
    if not symbol.isdigit() or len(symbol) != 6:
        raise ValueError(f"股票代码格式不正确: {symbol}，应为6位数字")
    
    # 验证报告期类型参数
    valid_indicators = {"按报告期", "按年度", "按单季度"}
    if indicator not in valid_indicators:
        raise ValueError(f"报告期类型不正确: {indicator}，应为 {valid_indicators}")
    
    try:
        logging.info(f"正在查询A股 {symbol} 的财务报表数据，报告期类型: {indicator}")
        
        # 调用akshare的三个财务报表接口
        balance_sheet_df = ak.stock_financial_debt_ths(symbol=symbol, indicator=indicator)
        income_statement_df = ak.stock_financial_benefit_ths(symbol=symbol, indicator=indicator)
        cash_flow_df = ak.stock_financial_cash_ths(symbol=symbol, indicator=indicator)
        
        # 格式化财务报表数据
        result = _format_a_stock_financial_report_data(
            balance_sheet_df, 
            income_statement_df, 
            cash_flow_df, 
            symbol, 
            indicator
        )
        
        logging.info(f"成功获取A股 {symbol} 的财务报表数据")
        return result
            
    except Exception as e:
        error_msg = f"获取A股 {symbol} 财务报表数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol, "indicator": indicator}


def _format_a_stock_financial_report_data(
    balance_sheet_df: DataFrame,
    income_statement_df: DataFrame, 
    cash_flow_df: DataFrame,
    symbol: str, 
    indicator: str
) -> Dict[str, Any]:
    """
    格式化A股财务报表数据，转换为更易读的结构
    
    Args:
        balance_sheet_df: 资产负债表数据
        income_statement_df: 利润表数据
        cash_flow_df: 现金流量表数据
        symbol: 股票代码
        indicator: 报告期类型
        
    Returns:
        Dict[str, Any]: 格式化后的财务报表数据
    """
    result = {
        "symbol": symbol,
        "indicator": indicator,
        "balance_sheet": {},
        "income_statement": {},
        "cash_flow": {}
    }
    
    # 处理资产负债表数据
    if isinstance(balance_sheet_df, DataFrame) and not balance_sheet_df.empty:
        balance_sheet_records = balance_sheet_df.to_dict('records')
        result["balance_sheet"] = {
            "records": balance_sheet_records,
            "total_records": len(balance_sheet_records),
            "columns": list(balance_sheet_df.columns)
        }
    else:
        result["balance_sheet"] = {"error": "未找到资产负债表数据"}
    
    # 处理利润表数据
    if isinstance(income_statement_df, DataFrame) and not income_statement_df.empty:
        income_statement_records = income_statement_df.to_dict('records')
        result["income_statement"] = {
            "records": income_statement_records,
            "total_records": len(income_statement_records),
            "columns": list(income_statement_df.columns)
        }
    else:
        result["income_statement"] = {"error": "未找到利润表数据"}
    
    # 处理现金流量表数据
    if isinstance(cash_flow_df, DataFrame) and not cash_flow_df.empty:
        cash_flow_records = cash_flow_df.to_dict('records')
        result["cash_flow"] = {
            "records": cash_flow_records,
            "total_records": len(cash_flow_records),
            "columns": list(cash_flow_df.columns)
        }
    else:
        result["cash_flow"] = {"error": "未找到现金流量表数据"}
    
    return result


@tool
def QueryHKStockFinacialReport(
    stock: str, 
    symbol: str = "资产负债表", 
    indicator: str = "年度"
) -> Dict[str, Any]:
    """
    查询港股财务报表数据
    
    Args:
        stock: 港股代码，例如 "00700" (腾讯控股)
        symbol: 报表类型，可选值: {"资产负债表", "利润表", "现金流量表"}，默认为 "资产负债表"
        indicator: 报告期类型，可选值: {"年度", "报告期"}，默认为 "年度"
        
    Returns:
        Dict[str, Any]: 包含财务报表数据的字典，如果查询失败则返回错误信息
        
    Raises:
        ValueError: 当参数为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    if not stock:
        raise ValueError("股票代码不能为空")
    
    # 验证报表类型参数
    valid_symbols = {"资产负债表", "利润表", "现金流量表"}
    if symbol not in valid_symbols:
        raise ValueError(f"报表类型不正确: {symbol}，应为 {valid_symbols}")
    
    # 验证报告期类型参数
    valid_indicators = {"年度", "报告期"}
    if indicator not in valid_indicators:
        raise ValueError(f"报告期类型不正确: {indicator}，应为 {valid_indicators}")
    
    try:
        logging.info(f"正在查询港股 {stock} 的财务报表数据，报表类型: {symbol}，报告期: {indicator}")
        
        # 调用akshare的stock_financial_hk_report_em接口
        financial_report_df = ak.stock_financial_hk_report_em(
            stock=stock,
            symbol=symbol,
            indicator=indicator
        )
        
        if isinstance(financial_report_df, DataFrame) and not financial_report_df.empty:
            # 格式化财务报表数据
            result = _format_hk_financial_report_data(financial_report_df, stock, symbol, indicator)
            logging.info(f"成功获取港股 {stock} 的财务报表数据，共 {len(financial_report_df)} 条记录")
            return result
        else:
            error_msg = f"未找到港股 {stock} 的财务报表数据"
            logging.warning(error_msg)
            return {"error": error_msg, "stock": stock, "symbol": symbol, "indicator": indicator}
            
    except Exception as e:
        error_msg = f"获取港股 {stock} 财务报表数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "stock": stock, "symbol": symbol, "indicator": indicator}


def _format_hk_financial_report_data(
    raw_df: DataFrame, 
    stock: str, 
    symbol: str, 
    indicator: str
) -> Dict[str, Any]:
    """
    格式化港股财务报表数据，转换为更易读的结构
    
    Args:
        raw_df: 原始DataFrame数据
        stock: 股票代码
        symbol: 报表类型
        indicator: 报告期类型
        
    Returns:
        Dict[str, Any]: 格式化后的财务报表数据
    """
    # 转换为字典列表
    records = raw_df.to_dict('records')
    
    # 按报告日期分组数据
    grouped_data = {}
    for record in records:
        report_date = record.get('REPORT_DATE')
        if report_date not in grouped_data:
            grouped_data[report_date] = []
        
        # 处理每个项目的数据
        item_data = {
            "std_item_name": record.get('STD_ITEM_NAME'),
            "amount": record.get('AMOUNT'),
            "std_item_code": record.get('STD_ITEM_CODE'),
            "fiscal_year": record.get('FISCAL_YEAR'),
            "date_type_code": record.get('DATE_TYPE_CODE')
        }
        grouped_data[report_date].append(item_data)
    
    # 构建结果
    result = {
        "stock": stock,
        "symbol": symbol,
        "indicator": indicator,
        "secucode": records[0].get('SECUCODE') if records else None,
        "security_code": records[0].get('SECURITY_CODE') if records else None,
        "security_name": records[0].get('SECURITY_NAME_ABBR') if records else None,
        "org_code": records[0].get('ORG_CODE') if records else None,
        "report_data": grouped_data,
        "total_records": len(records),
        "report_dates": list(grouped_data.keys())
    }
    
    return result


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
    records = raw_df.to_dict('records')
    
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
        "今开": "open"
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
        "open": "元"
    }
    
    return result
