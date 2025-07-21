#!/usr/bin/env python3
"""
模拟主程序环境，检查翻译器初始化
"""
import os
import asyncio
from dotenv import load_dotenv
from src.translation import KimiTranslator

# 模拟主程序加载顺序
print("=== 调试主程序环境 ===")

# 1. 检查加载前环境变量
print("1. 加载前环境变量:")
print(f"   KIMI_API_KEY: {os.getenv('KIMI_API_KEY')}")

# 2. 加载dotenv
load_dotenv()
print("2. 加载dotenv后:")
print(f"   KIMI_API_KEY: {os.getenv('KIMI_API_KEY')}")

# 3. 创建翻译器实例
print("3. 创建翻译器实例:")
try:
    translator = KimiTranslator()
    print(f"   翻译器.api_key: {translator.api_key}")
    print(f"   翻译器.base_url: {translator.base_url}")
    
    # 4. 测试翻译功能
    async def test_translate():
        print("4. 测试翻译功能:")
        result = await translator.translate("Hello, world")
        print(f"   翻译结果: {result}")
    
    asyncio.run(test_translate())
    
except Exception as e:
    print(f"   错误: {e}")
    import traceback
    traceback.print_exc()