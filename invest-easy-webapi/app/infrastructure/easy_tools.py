import os
from datetime import date

def write_file(tool_name:str, symbol: str, content:str):
    """
    将指定内容写入本地文件，用作缓存，以工具名称+股票代码作为文件名，也就是缓存的key。

    Args:
        tool_name: 必要参数，字符串类型，将要调用的工具的名称
        symbol: 必要参数，字符串类型，股票代码
        content: 必要参数，字符串类型，用于表示需要写入文档的具体内容。

    Returns:
        boolean: 是否写入成功

    Raises:
        ValueError: 当参数为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    filename = f"./cache/{date.today().strftime("%Y%m%d")}_{tool_name}_{symbol}.json"
    
    # 确保 cache 目录存在
    cache_dir = os.path.dirname(filename)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)

    if os.path.exists(filename):
        os.remove(filename)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return "已成功写入本地文件。"

def read_file(tool_name:str, symbol: str):
    """
    从本地文件中读取缓存的数据，以工具名称+股票代码作为文件名，也就是缓存的key。

    Args:
        tool_name: 必要参数，字符串类型，将要调用的工具的名称
        symbol: 必要参数，字符串类型，股票代码

    Returns:
        str: 如果找到了缓存文件则返回文件中的字符串数据，否则返回空字符串。

    Raises:
        ValueError: 当参数为空或格式不正确时
        RuntimeError: 当akshare API调用失败时
    """
    filename = f"./cache/{date.today().strftime("%Y%m%d")}_{tool_name}_{symbol}.json"
    
    # 检查文件是否存在，不存在则直接返回空字符串
    if not os.path.exists(filename):
        return ''
    
    content = ''
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    return content
