#!/usr/bin/env python3
"""
测试API密钥是否有效的脚本
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from src.translation import KimiTranslator

load_dotenv()

async def test_kimi_api():
    """测试Kimi API连接"""
    api_key = os.getenv("KIMI_API_KEY")
    if not api_key:
        print("❌ 未找到KIMI_API_KEY环境变量")
        return False
    
    print(f"🔑 使用API密钥: {api_key[:10]}...")
    
    translator = KimiTranslator(api_key=api_key)
    
    try:
        async with translator:
            success = await translator.test_connection()
            if success:
                print("✅ API连接测试成功")
                
                # 测试翻译功能
                test_text = "Hello, how are you?"
                translated = await translator.translate(test_text)
                if translated:
                    print(f"✅ 翻译测试成功: '{test_text}' -> '{translated}'")
                    return True
                else:
                    print("❌ 翻译测试失败")
                    return False
            else:
                print("❌ API连接测试失败 - 401 Unauthorized")
                print("💡 可能的原因:")
                print("   1. API密钥无效或已过期")
                print("   2. 账户余额不足")
                print("   3. API服务暂时不可用")
                return False
                
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_kimi_api())
    if result:
        print("\n🎉 API密钥有效，可以正常使用")
    else:
        print("\n⚠️  API密钥有问题，请检查配置")
    sys.exit(0 if result else 1)