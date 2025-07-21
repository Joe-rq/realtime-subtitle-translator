#!/usr/bin/env python3
"""
检查主程序的环境变量加载
"""
import os
from dotenv import load_dotenv

# 在main.py的相同位置测试
print("=== 主程序环境检查 ===")
print(f"1. 当前工作目录: {os.getcwd()}")
print(f"2. .env文件存在: {os.path.exists('.env')}")

# 加载环境变量
load_dotenv()
print(f"3. 加载后KIMI_API_KEY: {repr(os.getenv('KIMI_API_KEY'))}")
print(f"4. 密钥长度: {len(os.getenv('KIMI_API_KEY', ''))}")

# 检查是否被其他变量覆盖
for key in os.environ:
    if 'KIMI' in key.upper():
        print(f"5. 环境变量 {key}: {repr(os.environ[key])}")