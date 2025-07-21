#!/usr/bin/env python3
"""
调试API密钥问题的脚本
"""
import os
from dotenv import load_dotenv
from src.translation import KimiTranslator

# 加载环境变量
load_dotenv()

print("调试环境变量加载...")
print(f"KIMI_API_KEY 从环境变量读取: {os.getenv('KIMI_API_KEY', '未找到')}")

# 测试KimiTranslator初始化
try:
    translator = KimiTranslator()
    print(f"KimiTranslator 初始化成功")
    print(f"使用的API密钥: {translator.api_key[:10]}..." if translator.api_key else "API密钥为空")
except Exception as e:
    print(f"KimiTranslator 初始化失败: {e}")