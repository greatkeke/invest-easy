import logging
from typing import Dict, Any, List
import akshare as ak
from pandas import DataFrame


def GetStockGrowthComparison(symbol: str) -> Dict[str, Any]:
    """
    获取A股股票成长性比较数据（东方财富接口）

    Args:
        symbol: 证券代码，例如 "SZ000895"

    Returns:
        Dict[str, Any]: 包含成长性比较数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        logging.info(f"正在查询股票 {symbol} 的成长性比较数据...")

        # 调用akshare的stock_zh_growth_comparison_em接口
        growth_comparison_df = ak.stock_zh_growth_comparison_em(symbol=symbol)

        if isinstance(growth_comparison_df, DataFrame) and not growth_comparison_df.empty:
            # 格式化成长性比较数据
            result = _format_growth_comparison_data(growth_comparison_df, symbol)
            logging.info(f"成功获取股票 {symbol} 的成长性比较数据")
            return result
        else:
            error_msg = f"未找到股票 {symbol} 的成长性比较数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}

    except Exception as e:
        error_msg = f"获取股票 {symbol} 成长性比较数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def GetStockValuationComparison(symbol: str) -> Dict[str, Any]:
    """
    获取A股股票估值比较数据（东方财富接口）

    Args:
        symbol: 证券代码，例如 "SZ000895"

    Returns:
        Dict[str, Any]: 包含估值比较数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        logging.info(f"正在查询股票 {symbol} 的估值比较数据...")

        # 调用akshare的stock_zh_valuation_comparison_em接口
        valuation_comparison_df = ak.stock_zh_valuation_comparison_em(symbol=symbol)

        if isinstance(valuation_comparison_df, DataFrame) and not valuation_comparison_df.empty:
            # 格式化估值比较数据
            result = _format_valuation_comparison_data(valuation_comparison_df, symbol)
            logging.info(f"成功获取股票 {symbol} 的估值比较数据")
            return result
        else:
            error_msg = f"未找到股票 {symbol} 的估值比较数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}

    except Exception as e:
        error_msg = f"获取股票 {symbol} 估值比较数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def GetStockDupontComparison(symbol: str) -> Dict[str, Any]:
    """
    获取A股股票杜邦分析比较数据（东方财富接口）

    Args:
        symbol: 证券代码，例如 "SZ000895"

    Returns:
        Dict[str, Any]: 包含杜邦分析比较数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        logging.info(f"正在查询股票 {symbol} 的杜邦分析比较数据...")

        # 调用akshare的stock_zh_dupont_comparison_em接口
        dupont_comparison_df = ak.stock_zh_dupont_comparison_em(symbol=symbol)

        if isinstance(dupont_comparison_df, DataFrame) and not dupont_comparison_df.empty:
            # 格式化杜邦分析比较数据
            result = _format_dupont_comparison_data(dupont_comparison_df, symbol)
            logging.info(f"成功获取股票 {symbol} 的杜邦分析比较数据")
            return result
        else:
            error_msg = f"未找到股票 {symbol} 的杜邦分析比较数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}

    except Exception as e:
        error_msg = f"获取股票 {symbol} 杜邦分析比较数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def GetStockScaleComparison(symbol: str) -> Dict[str, Any]:
    """
    获取A股股票公司规模比较数据（东方财富接口）

    Args:
        symbol: 证券代码，例如 "SZ000895"

    Returns:
        Dict[str, Any]: 包含公司规模比较数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        logging.info(f"正在查询股票 {symbol} 的公司规模比较数据...")

        # 调用akshare的stock_zh_scale_comparison_em接口
        scale_comparison_df = ak.stock_zh_scale_comparison_em(symbol=symbol)

        if isinstance(scale_comparison_df, DataFrame) and not scale_comparison_df.empty:
            # 格式化公司规模比较数据
            result = _format_scale_comparison_data(scale_comparison_df, symbol)
            logging.info(f"成功获取股票 {symbol} 的公司规模比较数据")
            return result
        else:
            error_msg = f"未找到股票 {symbol} 的公司规模比较数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}

    except Exception as e:
        error_msg = f"获取股票 {symbol} 公司规模比较数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def GetHKStockGrowthComparison(symbol: str) -> Dict[str, Any]:
    """
    获取港股股票成长性比较数据（东方财富接口）

    Args:
        symbol: 证券代码，例如 "03900"

    Returns:
        Dict[str, Any]: 包含成长性比较数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        logging.info(f"正在查询港股 {symbol} 的成长性比较数据...")

        # 调用akshare的stock_hk_growth_comparison_em接口
        hk_growth_comparison_df = ak.stock_hk_growth_comparison_em(symbol=symbol)

        if isinstance(hk_growth_comparison_df, DataFrame) and not hk_growth_comparison_df.empty:
            # 格式化港股成长性比较数据
            result = _format_hk_growth_comparison_data(hk_growth_comparison_df, symbol)
            logging.info(f"成功获取港股 {symbol} 的成长性比较数据")
            return result
        else:
            error_msg = f"未找到港股 {symbol} 的成长性比较数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}

    except Exception as e:
        error_msg = f"获取港股 {symbol} 成长性比较数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def GetHKStockValuationComparison(symbol: str) -> Dict[str, Any]:
    """
    获取港股股票估值比较数据（东方财富接口）

    Args:
        symbol: 证券代码，例如 "03900"

    Returns:
        Dict[str, Any]: 包含估值比较数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        logging.info(f"正在查询港股 {symbol} 的估值比较数据...")

        # 调用akshare的stock_hk_valuation_comparison_em接口
        hk_valuation_comparison_df = ak.stock_hk_valuation_comparison_em(symbol=symbol)

        if isinstance(hk_valuation_comparison_df, DataFrame) and not hk_valuation_comparison_df.empty:
            # 格式化港股估值比较数据
            result = _format_hk_valuation_comparison_data(hk_valuation_comparison_df, symbol)
            logging.info(f"成功获取港股 {symbol} 的估值比较数据")
            return result
        else:
            error_msg = f"未找到港股 {symbol} 的估值比较数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}

    except Exception as e:
        error_msg = f"获取港股 {symbol} 估值比较数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def GetHKStockScaleComparison(symbol: str) -> Dict[str, Any]:
    """
    获取港股股票公司规模比较数据（东方财富接口）

    Args:
        symbol: 证券代码，例如 "03900"

    Returns:
        Dict[str, Any]: 包含公司规模比较数据的字典，如果查询失败则返回错误信息

    Raises:
        ValueError: 当symbol为空时
        RuntimeError: 当akshare API调用失败时
    """
    if not symbol:
        raise ValueError("股票代码不能为空")

    try:
        logging.info(f"正在查询港股 {symbol} 的公司规模比较数据...")

        # 调用akshare的stock_hk_scale_comparison_em接口
        hk_scale_comparison_df = ak.stock_hk_scale_comparison_em(symbol=symbol)

        if isinstance(hk_scale_comparison_df, DataFrame) and not hk_scale_comparison_df.empty:
            # 格式化港股公司规模比较数据
            result = _format_hk_scale_comparison_data(hk_scale_comparison_df, symbol)
            logging.info(f"成功获取港股 {symbol} 的公司规模比较数据")
            return result
        else:
            error_msg = f"未找到港股 {symbol} 的公司规模比较数据"
            logging.warning(error_msg)
            return {"error": error_msg, "symbol": symbol}

    except Exception as e:
        error_msg = f"获取港股 {symbol} 公司规模比较数据失败: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg, "symbol": symbol}


def _format_growth_comparison_data(raw_df: DataFrame, symbol: str) -> Dict[str, Any]:
    """
    格式化成长性比较数据

    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码

    Returns:
        Dict[str, Any]: 格式化后的成长性比较数据
    """
    # 转换为字典列表
    records = raw_df.to_dict("records")

    if not records:
        return {"error": "未找到成长性比较数据", "symbol": symbol}

    # 构建结果
    result: Dict[str, Any] = {
        "symbol": symbol,
        "comparison_data": []
    }

    for record in records:
        formatted_record = {
            "symbol": record.get("代码", ""),
            "name": record.get("简称", ""),
            "eps_growth_3y_compound": record.get("基本每股收益增长率-3年复合"),
            "eps_growth_24a": record.get("基本每股收益增长率-24A"),
            "eps_growth_ttm": record.get("基本每股收益增长率-TTM"),
            "eps_growth_25e": record.get("基本每股收益增长率-25E"),
            "eps_growth_26e": record.get("基本每股收益增长率-26E"),
            "eps_growth_27e": record.get("基本每股收益增长率-27E"),
            "revenue_growth_3y_compound": record.get("营业收入增长率-3年复合"),
            "revenue_growth_24a": record.get("营业收入增长率-24A"),
            "revenue_growth_ttm": record.get("营业收入增长率-TTM"),
            "revenue_growth_25e": record.get("营业收入增长率-25E"),
            "revenue_growth_26e": record.get("营业收入增长率-26E"),
            "revenue_growth_27e": record.get("营业收入增长率-27E"),
            "net_profit_growth_3y_compound": record.get("净利润增长率-3年复合"),
            "net_profit_growth_24a": record.get("净利润增长率-24A"),
            "net_profit_growth_ttm": record.get("净利润增长率-TTM"),
            "net_profit_growth_25e": record.get("净利润增长率-25E"),
            "net_profit_growth_26e": record.get("净利润增长率-26E"),
            "net_profit_growth_27e": record.get("净利润增长率-27E"),
            "eps_growth_3y_compound_rank": record.get("基本每股收益增长率-3年复合排名")
        }
        result["comparison_data"].append(formatted_record)

    # 添加单位说明
    result["units"] = {
        "eps_growth_3y_compound": "%",
        "eps_growth_24a": "%",
        "eps_growth_ttm": "%",
        "eps_growth_25e": "%",
        "eps_growth_26e": "%",
        "eps_growth_27e": "%",
        "revenue_growth_3y_compound": "%",
        "revenue_growth_24a": "%",
        "revenue_growth_ttm": "%",
        "revenue_growth_25e": "%",
        "revenue_growth_26e": "%",
        "revenue_growth_27e": "%",
        "net_profit_growth_3y_compound": "%",
        "net_profit_growth_24a": "%",
        "net_profit_growth_ttm": "%",
        "net_profit_growth_25e": "%",
        "net_profit_growth_26e": "%",
        "net_profit_growth_27e": "%"
    }

    return result


def _format_valuation_comparison_data(raw_df: DataFrame, symbol: str) -> Dict[str, Any]:
    """
    格式化估值比较数据

    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码

    Returns:
        Dict[str, Any]: 格式化后的估值比较数据
    """
    # 转换为字典列表
    records = raw_df.to_dict("records")

    if not records:
        return {"error": "未找到估值比较数据", "symbol": symbol}

    # 构建结果
    result: Dict[str, Any] = {
        "symbol": symbol,
        "comparison_data": []
    }

    for record in records:
        formatted_record = {
            "symbol": record.get("代码", ""),
            "name": record.get("简称", ""),
            "peg": record.get("PEG"),
            "pe_24a": record.get("市盈率-24A"),
            "pe_ttm": record.get("市盈率-TTM"),
            "pe_25e": record.get("市盈率-25E"),
            "pe_26e": record.get("市盈率-26E"),
            "pe_27e": record.get("市盈率-27E"),
            "ps_24a": record.get("市销率-24A"),
            "ps_ttm": record.get("市销率-TTM"),
            "ps_25e": record.get("市销率-25E"),
            "ps_26e": record.get("市销率-26E"),
            "ps_27e": record.get("市销率-27E"),
            "pb_24a": record.get("市净率-24A"),
            "pb_mrq": record.get("市净率-MRQ"),
            "pce_24a": record.get("市现率PCE-24A"),
            "pce_ttm": record.get("市现率PCE-TTM"),
            "pcf_24a": record.get("市现率PCF-24A"),
            "pcf_ttm": record.get("市现率PCF-TTM"),
            "ev_ebitda_24a": record.get("EV/EBITDA-24A"),
            "peg_rank": record.get("PEG排名")
        }
        result["comparison_data"].append(formatted_record)

    # 添加单位说明
    result["units"] = {
        "peg": "倍",
        "pe_24a": "倍",
        "pe_ttm": "倍",
        "pe_25e": "倍",
        "pe_26e": "倍",
        "pe_27e": "倍",
        "ps_24a": "倍",
        "ps_ttm": "倍",
        "ps_25e": "倍",
        "ps_26e": "倍",
        "ps_27e": "倍",
        "pb_24a": "倍",
        "pb_mrq": "倍",
        "pce_24a": "倍",
        "pce_ttm": "倍",
        "pcf_24a": "倍",
        "pcf_ttm": "倍",
        "ev_ebitda_24a": "倍"
    }

    return result


def _format_dupont_comparison_data(raw_df: DataFrame, symbol: str) -> Dict[str, Any]:
    """
    格式化杜邦分析比较数据

    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码

    Returns:
        Dict[str, Any]: 格式化后的杜邦分析比较数据
    """
    # 转换为字典列表
    records = raw_df.to_dict("records")

    if not records:
        return {"error": "未找到杜邦分析比较数据", "symbol": symbol}

    # 构建结果
    result: Dict[str, Any] = {
        "symbol": symbol,
        "comparison_data": []
    }

    for record in records:
        formatted_record = {
            "symbol": record.get("代码", ""),
            "name": record.get("简称", ""),
            "roe_3y_avg": record.get("ROE-3年平均"),
            "roe_22a": record.get("ROE-22A"),
            "roe_23a": record.get("ROE-23A"),
            "roe_24a": record.get("ROE-24A"),
            "net_margin_3y_avg": record.get("净利率-3年平均"),
            "net_margin_22a": record.get("净利率-22A"),
            "net_margin_23a": record.get("净利率-23A"),
            "net_margin_24a": record.get("净利率-24A"),
            "asset_turnover_3y_avg": record.get("总资产周转率-3年平均"),
            "asset_turnover_22a": record.get("总资产周转率-22A"),
            "asset_turnover_23a": record.get("总资产周转率-23A"),
            "asset_turnover_24a": record.get("总资产周转率-24A"),
            "equity_multiplier_3y_avg": record.get("权益乘数-3年平均"),
            "equity_multiplier_22a": record.get("权益乘数-22A"),
            "equity_multiplier_23a": record.get("权益乘数-23A"),
            "equity_multiplier_24a": record.get("权益乘数-24A"),
            "roe_3y_avg_rank": record.get("ROE-3年平均排名")
        }
        result["comparison_data"].append(formatted_record)

    # 添加单位说明
    result["units"] = {
        "roe_3y_avg": "%",
        "roe_22a": "%",
        "roe_23a": "%",
        "roe_24a": "%",
        "net_margin_3y_avg": "%",
        "net_margin_22a": "%",
        "net_margin_23a": "%",
        "net_margin_24a": "%",
        "asset_turnover_3y_avg": "次",
        "asset_turnover_22a": "次",
        "asset_turnover_23a": "次",
        "asset_turnover_24a": "次",
        "equity_multiplier_3y_avg": "倍",
        "equity_multiplier_22a": "倍",
        "equity_multiplier_23a": "倍",
        "equity_multiplier_24a": "倍"
    }

    return result


def _format_scale_comparison_data(raw_df: DataFrame, symbol: str) -> Dict[str, Any]:
    """
    格式化公司规模比较数据

    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码

    Returns:
        Dict[str, Any]: 格式化后的公司规模比较数据
    """
    # 转换为字典列表
    records = raw_df.to_dict("records")

    if not records:
        return {"error": "未找到公司规模比较数据", "symbol": symbol}

    # 构建结果
    result: Dict[str, Any] = {
        "symbol": symbol,
        "comparison_data": []
    }

    for record in records:
        formatted_record = {
            "symbol": record.get("代码", ""),
            "name": record.get("简称", ""),
            "total_market_cap": record.get("总市值"),
            "total_market_cap_rank": record.get("总市值排名"),
            "circulating_market_cap": record.get("流通市值"),
            "circulating_market_cap_rank": record.get("流通市值排名"),
            "revenue": record.get("营业收入"),
            "revenue_rank": record.get("营业收入排名"),
            "net_profit": record.get("净利润"),
            "net_profit_rank": record.get("净利润排名")
        }
        result["comparison_data"].append(formatted_record)

    # 添加单位说明
    result["units"] = {
        "total_market_cap": "元",
        "circulating_market_cap": "元",
        "revenue": "元",
        "net_profit": "元"
    }

    return result


def _format_hk_growth_comparison_data(raw_df: DataFrame, symbol: str) -> Dict[str, Any]:
    """
    格式化港股成长性比较数据

    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码

    Returns:
        Dict[str, Any]: 格式化后的港股成长性比较数据
    """
    # 转换为字典列表
    records = raw_df.to_dict("records")

    if not records:
        return {"error": "未找到港股成长性比较数据", "symbol": symbol}

    # 构建结果
    result: Dict[str, Any] = {
        "symbol": symbol,
        "comparison_data": []
    }

    for record in records:
        formatted_record = {
            "symbol": record.get("代码", ""),
            "name": record.get("简称", ""),
            "eps_growth_yoy": record.get("基本每股收益同比增长率"),
            "eps_growth_yoy_rank": record.get("基本每股收益同比增长率排名"),
            "revenue_growth_yoy": record.get("营业收入同比增长率"),
            "revenue_growth_yoy_rank": record.get("营业收入同比增长率排名"),
            "operating_margin_growth_yoy": record.get("营业利润率同比增长率"),
            "operating_margin_growth_yoy_rank": record.get("营业利润率同比增长率排名"),
            "total_assets_growth_yoy": record.get("基本每股收总资产同比增长率益同比增长率"),
            "total_assets_growth_yoy_rank": record.get("总资产同比增长率排名")
        }
        result["comparison_data"].append(formatted_record)

    # 添加单位说明
    result["units"] = {
        "eps_growth_yoy": "%",
        "revenue_growth_yoy": "%",
        "operating_margin_growth_yoy": "%",
        "total_assets_growth_yoy": "%"
    }

    return result


def _format_hk_valuation_comparison_data(raw_df: DataFrame, symbol: str) -> Dict[str, Any]:
    """
    格式化港股估值比较数据

    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码

    Returns:
        Dict[str, Any]: 格式化后的港股估值比较数据
    """
    # 转换为字典列表
    records = raw_df.to_dict("records")

    if not records:
        return {"error": "未找到港股估值比较数据", "symbol": symbol}

    # 构建结果
    result: Dict[str, Any] = {
        "symbol": symbol,
        "comparison_data": []
    }

    for record in records:
        formatted_record = {
            "symbol": record.get("代码", ""),
            "name": record.get("简称", ""),
            "pe_ttm": record.get("市盈率-TTM"),
            "pe_ttm_rank": record.get("市盈率-TTM排名"),
            "pe_lyr": record.get("市盈率-LYR"),
            "pe_lyr_rank": record.get("市盈率-LYR排名"),
            "pb_mrq": record.get("市净率-MRQ"),
            "pb_mrq_rank": record.get("市净率-MRQ排名"),
            "pb_lyr": record.get("市净率-LYR"),
            "pb_lyr_rank": record.get("市净率-LYR排名"),
            "ps_ttm": record.get("市销率-TTM"),
            "ps_ttm_rank": record.get("市销率-TTM排名"),
            "ps_lyr": record.get("市销率-LYR"),
            "ps_lyr_rank": record.get("市销率-LYR排名"),
            "pcf_ttm": record.get("市现率-TTM"),
            "pcf_ttm_rank": record.get("市现率-TTM排名"),
            "pcf_lyr": record.get("市现率-LYR"),
            "pcf_lyr_rank": record.get("市现率-LYR排名")
        }
        result["comparison_data"].append(formatted_record)

    # 添加单位说明
    result["units"] = {
        "pe_ttm": "倍",
        "pe_lyr": "倍",
        "pb_mrq": "倍",
        "pb_lyr": "倍",
        "ps_ttm": "倍",
        "ps_lyr": "倍",
        "pcf_ttm": "倍",
        "pcf_lyr": "倍"
    }

    return result


def _format_hk_scale_comparison_data(raw_df: DataFrame, symbol: str) -> Dict[str, Any]:
    """
    格式化港股公司规模比较数据

    Args:
        raw_df: 原始DataFrame数据
        symbol: 股票代码

    Returns:
        Dict[str, Any]: 格式化后的港股公司规模比较数据
    """
    # 转换为字典列表
    records = raw_df.to_dict("records")

    if not records:
        return {"error": "未找到港股公司规模比较数据", "symbol": symbol}

    # 构建结果
    result: Dict[str, Any] = {
        "symbol": symbol,
        "comparison_data": []
    }

    for record in records:
        formatted_record = {
            "symbol": record.get("代码", ""),
            "name": record.get("简称", ""),
            "total_market_cap": record.get("总市值"),
            "total_market_cap_rank": record.get("总市值排名"),
            "circulating_market_cap": record.get("流通市值"),
            "circulating_market_cap_rank": record.get("流通市值排名"),
            "total_revenue": record.get("营业总收入"),
            "total_revenue_rank": record.get("营业总收入排名"),
            "net_profit": record.get("净利润"),
            "net_profit_rank": record.get("净利润排名")
        }
        result["comparison_data"].append(formatted_record)

    # 添加单位说明
    result["units"] = {
        "total_market_cap": "港元",
        "circulating_market_cap": "港元",
        "total_revenue": "港元",
        "net_profit": "港元"
    }

    return result
