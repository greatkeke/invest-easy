import logging
from typing import Dict, Any
import akshare as ak
from pandas import DataFrame

def GetUSStockFinacialReport(
    stock: str, 
    symbol: str = "资产负债表", 
    indicator: str = "单季报"
) -> Dict[str, Any]:
    """
    查询美股财务报表数据
    
    Args:
        stock: 美股代码，例如 "TSLA" 或 "BRK_A"（注意：BRK.A 需要转换为 BRK_A）
        symbol: 报表类型，可选值: {"资产负债表", "综合损益表", "现金流量表"}，默认为 "资产负债表"
        indicator: 报告期类型，可选值: {"年报", "单季报", "累计季报"}，默认为 "单季报"
        
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
            financial_report_df = financial_report_df[:30]
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


def GetAStockFinacialReport(
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
            balance_sheet_df[:10], 
            income_statement_df[:10], 
            cash_flow_df[:10], 
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


def GetHKStockFinacialReport(
    stock: str, 
    symbol: str = "资产负债表", 
    indicator: str = "报告期"
) -> Dict[str, Any]:
    """
    查询港股财务报表数据
    
    Args:
        stock: 港股代码，例如 "00700" (腾讯控股)
        symbol: 报表类型，可选值: {"资产负债表", "利润表", "现金流量表"}，默认为 "资产负债表"
        indicator: 报告期类型，可选值: {"年度", "报告期"}，默认为 "报告期"
        
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
            financial_report_df = financial_report_df[:100]
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