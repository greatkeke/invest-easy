#!/usr/bin/env python3
"""
测试流式响应功能的脚本
"""

import asyncio
import aiohttp
import json

async def test_streaming_response():
    """测试流式响应功能"""
    url = "http://localhost:8000/reports/generate/00700"  # 测试腾讯控股
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/plain"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as response:
                print(f"状态码: {response.status}")
                print(f"响应头: {dict(response.headers)}")
                print("\n开始接收流式数据:\n")
                
                # 逐块读取流式响应
                async for chunk in response.content:
                    if chunk:
                        text = chunk.decode('utf-8')
                        print(f"收到数据块: {text.strip()}")
                        
                        # 如果收到结束标记，停止读取
                        if "[DONE]" in text:
                            print("\n流式响应结束")
                            break
                            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    print("开始测试流式响应功能...")
    asyncio.run(test_streaming_response())
