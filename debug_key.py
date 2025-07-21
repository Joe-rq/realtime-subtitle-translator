#!/usr/bin/env python3
"""
调试API密钥的详细验证脚本
"""
import os
import asyncio
import aiohttp
from dotenv import load_dotenv
from src.translation import KimiTranslator

# 加载环境变量
load_dotenv()

print("=== 调试API密钥 ===")
print(f"环境变量中的KIMI_API_KEY: {repr(os.getenv('KIMI_API_KEY'))}")
print(f"环境变量长度: {len(os.getenv('KIMI_API_KEY', ''))}")

# 创建翻译器实例
translator = KimiTranslator()
print(f"翻译器中的API密钥: {repr(translator.api_key)}")
print(f"翻译器API密钥长度: {len(translator.api_key or '')}")

# 检查密钥格式
key = os.getenv('KIMI_API_KEY')
if key:
    print(f"密钥前缀: {key[:10]}")
    print(f"密钥后缀: {key[-10:]}")
    print(f"密钥包含空格: {' ' in key}")
    newline_char = '\n'
    print(f"密钥包含换行符: {newline_char in key}")

# 测试API连接
async def test_api():
    try:
        result = await translator.test_connection()
        print(f"API连接测试结果: {result}")
        
        if result:
            # 测试翻译
            translation = await translator.translate("Hello world")
            print(f"翻译测试结果: {translation}")
        else:
            print("API连接失败，检查密钥和网络")
            
    except Exception as e:
        print(f"测试异常: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())