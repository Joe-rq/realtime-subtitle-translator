#!/usr/bin/env python3
"""
测试翻译功能的完整脚本
"""
import asyncio
import os
from dotenv import load_dotenv
from src.translation import KimiTranslator

# 加载环境变量
load_dotenv()

async def test_translation():
    """测试翻译功能"""
    print("=== 测试翻译功能 ===")
    
    try:
        # 初始化翻译器
        translator = KimiTranslator()
        print(f"✅ 翻译器初始化成功")
        print(f"API密钥: {translator.api_key[:15]}...")
        print(f"基础URL: {translator.base_url}")
        
        # 测试翻译
        test_text = "Hello, how are you?"
        print(f"测试文本: {test_text}")
        
        result = await translator.translate(test_text)
        if result:
            print(f"✅ 翻译结果: {result}")
        else:
            print("❌ 翻译返回空结果")
            
    except Exception as e:
        print(f"❌ 翻译测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_translation())