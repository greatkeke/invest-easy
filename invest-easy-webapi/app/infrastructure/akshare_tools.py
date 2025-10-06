import logging
from typing import Dict, Any, Optional, Union, List
import akshare as ak
from pandas import DataFrame
from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field

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
