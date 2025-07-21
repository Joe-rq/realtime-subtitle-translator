#!/usr/bin/env python3
"""
验证特定API密钥的脚本
"""
import os
import asyncio
import aiohttp

async def test_specific_key():
    """测试特定的Kimi API密钥"""
    
    # 使用.env文件中的确切密钥
    api_key = "sk-Ff88cotwDOFGVtooQpR0EuZXTbsb3eVDs4cIygijoF7oJUj3"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 测试API连接
    url = "https://api.moonshot.cn/v1/models"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                print(f"状态码: {response.status}")
                text = await response.text()
                print(f"响应: {text}")
                
                if response.status == 200:
                    print("✅ API密钥有效")
                    return True
                else:
                    print("❌ API密钥无效")
                    return False
                    
        except Exception as e:
            print(f"请求错误: {e}")
            return False

if __name__ == "__main__":
    asyncio.run(test_specific_key())