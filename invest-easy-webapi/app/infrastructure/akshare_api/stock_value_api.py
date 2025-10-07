import logging
from typing import Dict, Any
import akshare as ak
from pandas import DataFrame


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


def GetStockValue(symbol: str) -> Dict[str, Any]:
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
