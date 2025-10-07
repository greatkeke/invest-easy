import logging
from typing import Dict, Any
import akshare as ak
from pandas import DataFrame
from datetime import datetime
import re


def _calculate_date_difference(start_date: str, end_date: str) -> int:
    """
    计算两个日期之间的天数差
    
    Args:
        start_date: 开始日期，格式为 "YYYYMMDD"
        end_date: 结束日期，格式为 "YYYYMMDD"
        
    Returns:
        int: 天数差
    """
    try:
        start_dt = datetime.strptime(start_date, "%Y%m%d")
        end_dt = datetime.strptime(end_date, "%Y%m%d")
        return (end_dt - start_dt).days
    except ValueError as e:
        raise ValueError(f"日期格式不正确: {e}")


def _determine_period(start_date: str, end_date: str) -> str:
    """
    根据时间跨度自动确定数据频率
    
    Args:
        start_date: 开始日期，格式为 "YYYYMMDD"
        end_date: 结束日期，格式为 "YYYYMMDD"
        
    Returns:
        str: 数据频率，'daily', 'weekly', 或 'monthly'
    """
    days_diff = _calculate_date_difference(start_date, end_date)
    
    if days_diff > 365:  # 大于一年
        return "monthly"
    elif days_diff > 30:  # 大于一个月
        return "weekly"
    else:  # 一个月以内
        return "daily"


def _detect_market(symbol: str) -> str:
    """
    根据股票代码检测市场类型
    
    Args:
        symbol: 股票代码
        
    Returns:
        str: 市场类型，'A', 'US', 或 'HK'
    """
    # 美股检测（字母代码）
    if re.match(r'^[A-Z]+$', symbol):
        return "US"
    
    # 港股检测（5位数字代码）
    elif re.match(r'^\d{5}$', symbol):
        return "HK"
    
    # A股检测（6位数字代码）
    elif re.match(r'^\d{6}$', symbol):
        return "A"
    
    else:
        raise ValueError(f"无法识别股票代码 {symbol} 的市场类型")


def GetStockHistoricalData(
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
        adjust: 复权类型，可选值: {"", "qfq", "hfq"}，默认为 "" (qfq)
        period: 数据频率，可选值: {"auto", "daily", "weekly", "monthly"}，默认为 "auto" (自动选择)
        
    Returns:
        Dict[str, Any]: 包含历史行情数据的字典，如果查询失败则返回错误信息
        
    Raises:
        ValueError: 当参数为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")
    
    if not start_date or not end_date:
        raise ValueError("开始日期和结束日期不能为空")
    
    # 验证日期格式
    try:
        datetime.strptime(start_date, "%Y%m%d")
        datetime.strptime(end_date, "%Y%m%d")
    except ValueError:
        raise ValueError("日期格式不正确，应为 YYYYMMDD 格式")
    
    # 验证复权类型参数
    valid_adjusts = {"", "qfq", "hfq"}
    if adjust not in valid_adjusts:
        raise ValueError(f"复权类型不正确: {adjust}，应为 {valid_adjusts}")
    
    # 验证数据频率参数
    valid_periods = {"auto", "daily", "weekly", "monthly"}
    if period not in valid_periods:
        raise ValueError(f"数据频率不正确: {period}，应为 {valid_periods}")
    
    try:
        # 检测市场类型
        market = _detect_market(symbol)
        logging.info(f"检测到股票 {symbol} 属于 {market} 市场")
        
        # 自动确定数据频率
        if period == "auto":
            period = _determine_period(start_date, end_date)
            logging.info(f"根据时间跨度自动选择数据频率: {period}")
        
        # 根据市场类型调用不同的API
        if market == "A":
            return _query_a_stock_historical_data(symbol, period, start_date, end_date, adjust)
        elif market == "US":
            return _query_us_stock_historical_data(symbol, adjust)
        elif market == "HK":
            return _query_hk_stock_historical_data(symbol, period, start_date, end_date, adjust)
        else:
            raise ValueError(f"不支持的市场类型: {market}")
            
    except Exception as e:
        error_msg = f"获取股票 {symbol} 历史行情数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol, "start_date": start_date, "end_date": end_date}


def _query_a_stock_historical_data(
    symbol: str, 
    period: str, 
    start_date: str, 
    end_date: str, 
    adjust: str
) -> Dict[str, Any]:
    """
    查询沪深京A股历史行情数据
    
    Args:
        symbol: A股代码
        period: 数据频率
        start_date: 开始日期
        end_date: 结束日期
        adjust: 复权类型
        
    Returns:
        Dict[str, Any]: 格式化后的历史行情数据
    """
    logging.info(f"正在查询A股 {symbol} 的历史行情数据，频率: {period}，日期范围: {start_date} 至 {end_date}")
    
    # 调用akshare的stock_zh_a_hist接口
    stock_hist_df = ak.stock_zh_a_hist(
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
        adjust=adjust
    )
    
    if isinstance(stock_hist_df, DataFrame) and not stock_hist_df.empty:
        # 格式化历史行情数据
        result = _format_a_stock_historical_data(stock_hist_df, symbol, period, adjust)
        logging.info(f"成功获取A股 {symbol} 的历史行情数据，共 {len(stock_hist_df)} 条记录")
        return result
    else:
        error_msg = f"未找到A股 {symbol} 的历史行情数据"
        logging.warning(error_msg)
        return {"error": error_msg, "symbol": symbol, "period": period, "start_date": start_date, "end_date": end_date}


def _query_us_stock_historical_data(symbol: str, adjust: str) -> Dict[str, Any]:
    """
    查询美股历史行情数据
    
    Args:
        symbol: 美股代码
        adjust: 复权类型
        
    Returns:
        Dict[str, Any]: 格式化后的历史行情数据
    """
    logging.info(f"正在查询美股 {symbol} 的历史行情数据")
    
    # 调用akshare的stock_us_daily接口
    stock_hist_df = ak.stock_us_daily(symbol=symbol, adjust=adjust)
    
    if isinstance(stock_hist_df, DataFrame) and not stock_hist_df.empty:
        # 按日期排序并获取最新的50条数据
        if 'date' in stock_hist_df.columns:
            stock_hist_df = stock_hist_df.sort_values('date', ascending=False).head(50)
        else:
            stock_hist_df = stock_hist_df.head(50)
        result = _format_us_stock_historical_data(stock_hist_df, symbol, adjust)
        logging.info(f"成功获取美股 {symbol} 的历史行情数据，共 {len(stock_hist_df)} 条记录")
        return result
    else:
        error_msg = f"未找到美股 {symbol} 的历史行情数据"
        logging.warning(error_msg)
        return {"error": error_msg, "symbol": symbol}


def _query_hk_stock_historical_data(
    symbol: str, 
    period: str, 
    start_date: str, 
    end_date: str, 
    adjust: str
) -> Dict[str, Any]:
    """
    查询港股历史行情数据
    
    Args:
        symbol: 港股代码
        period: 数据频率
        start_date: 开始日期
        end_date: 结束日期
        adjust: 复权类型
        
    Returns:
        Dict[str, Any]: 格式化后的历史行情数据
    """
    logging.info(f"正在查询港股 {symbol} 的历史行情数据，频率: {period}，日期范围: {start_date} 至 {end_date}")
    
    # 调用akshare的stock_hk_hist接口
    stock_hist_df = ak.stock_hk_hist(
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
        adjust=adjust
    )
    
    if isinstance(stock_hist_df, DataFrame) and not stock_hist_df.empty:
        # 格式化历史行情数据
        result = _format_hk_stock_historical_data(stock_hist_df, symbol, period, adjust)
        logging.info(f"成功获取港股 {symbol} 的历史行情数据，共 {len(stock_hist_df)} 条记录")
        return result
    else:
        error_msg = f"未找到港股 {symbol} 的历史行情数据"
        logging.warning(error_msg)
        return {"error": error_msg, "symbol": symbol, "period": period, "start_date": start_date, "end_date": end_date}


def _format_a_stock_historical_data(
    raw_df: DataFrame, 
    symbol: str, 
    period: str, 
    adjust: str
) -> Dict[str, Any]:
    """
    格式化沪深京A股历史行情数据
    
    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码
        period: 数据频率
        adjust: 复权类型
        
    Returns:
        Dict[str, Any]: 格式化后的历史行情数据
    """
    # 转换为字典列表
    records = raw_df.to_dict('records')
    
    # 中文到英文字段名映射
    field_mapping = {
        "日期": "date",
        "股票代码": "symbol",
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "volume",
        "成交额": "turnover",
        "振幅": "amplitude",
        "涨跌幅": "change_percent",
        "涨跌额": "change_amount",
        "换手率": "turnover_rate"
    }
    
    # 格式化记录
    formatted_records = []
    for record in records:
        formatted_record = {}
        for chinese_field, english_field in field_mapping.items():
            value = record.get(chinese_field)
            # 处理特殊值（NaN等）
            if isinstance(value, float) and (value != value):  # 检查NaN
                formatted_record[english_field] = None
            else:
                formatted_record[english_field] = value
        formatted_records.append(formatted_record)
    
    # 构建结果
    result = {
        "symbol": symbol,
        "market": "A",
        "period": period,
        "adjust": adjust,
        "total_records": len(formatted_records),
        "data": formatted_records,
        "units": {
            "open": "元",
            "close": "元",
            "high": "元",
            "low": "元",
            "volume": "手",
            "turnover": "元",
            "amplitude": "%",
            "change_percent": "%",
            "change_amount": "元",
            "turnover_rate": "%"
        }
    }
    
    return result


def _format_us_stock_historical_data(
    raw_df: DataFrame, 
    symbol: str, 
    adjust: str
) -> Dict[str, Any]:
    """
    格式化美股历史行情数据
    
    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码
        adjust: 复权类型
        
    Returns:
        Dict[str, Any]: 格式化后的历史行情数据
    """
    # 转换为字典列表
    records = raw_df.to_dict('records')
    
    # 格式化记录
    formatted_records = []
    for record in records:
        formatted_record = {
            "date": record.get("date"),
            "open": record.get("open"),
            "high": record.get("high"),
            "low": record.get("low"),
            "close": record.get("close"),
            "volume": record.get("volume")
        }
        formatted_records.append(formatted_record)
    
    # 构建结果
    result = {
        "symbol": symbol,
        "market": "US",
        "period": "daily",  # 美股只有日线数据
        "adjust": adjust,
        "total_records": len(formatted_records),
        "data": formatted_records,
        "units": {
            "open": "美元",
            "high": "美元",
            "low": "美元",
            "close": "美元",
            "volume": "股"
        }
    }
    
    return result


def _format_hk_stock_historical_data(
    raw_df: DataFrame, 
    symbol: str, 
    period: str, 
    adjust: str
) -> Dict[str, Any]:
    """
    格式化港股历史行情数据
    
    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码
        period: 数据频率
        adjust: 复权类型
        
    Returns:
        Dict[str, Any]: 格式化后的历史行情数据
    """
    # 转换为字典列表
    records = raw_df.to_dict('records')
    
    # 中文到英文字段名映射
    field_mapping = {
        "日期": "date",
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "volume",
        "成交额": "turnover",
        "振幅": "amplitude",
        "涨跌幅": "change_percent",
        "涨跌额": "change_amount",
        "换手率": "turnover_rate"
    }
    
    # 格式化记录
    formatted_records = []
    for record in records:
        formatted_record = {}
        for chinese_field, english_field in field_mapping.items():
            value = record.get(chinese_field)
            # 处理特殊值（NaN等）
            if isinstance(value, float) and (value != value):  # 检查NaN
                formatted_record[english_field] = None
            else:
                formatted_record[english_field] = value
        formatted_records.append(formatted_record)
    
    # 构建结果
    result = {
        "symbol": symbol,
        "market": "HK",
        "period": period,
        "adjust": adjust,
        "total_records": len(formatted_records),
        "data": formatted_records,
        "units": {
            "open": "港元",
            "close": "港元",
            "high": "港元",
            "low": "港元",
            "volume": "股",
            "turnover": "港元",
            "amplitude": "%",
            "change_percent": "%",
            "change_amount": "港元",
            "turnover_rate": "%"
        }
    }
    
    return result
