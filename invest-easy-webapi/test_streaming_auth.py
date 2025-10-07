#!/usr/bin/env python3
"""
测试流式响应功能的脚本（带认证）
"""

import asyncio
import aiohttp
import json

async def get_auth_token():
    """获取认证token"""
    login_url = "http://localhost:8000/api/auth/jwt/login"
    login_data = {
        "username": "agg@agg.com",  # 使用默认测试用户
        "password": "123"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(login_url, data=login_data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("access_token")
                else:
                    print(f"登录失败: {response.status}")
                    return None
    except Exception as e:
        print(f"获取token失败: {e}")
        return None

async def test_streaming_response():
    """测试流式响应功能"""
    # 首先获取认证token
    token = await get_auth_token()
    if not token:
        print("无法获取认证token，请检查用户凭据")
        return
    
    url = "http://localhost:8000/api/reports/generate/00700"  # 注意完整的API路径
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/plain",
        "Authorization": f"Bearer {token}"
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
    print("开始测试流式响应功能（带认证）...")
    asyncio.run(test_streaming_response())
