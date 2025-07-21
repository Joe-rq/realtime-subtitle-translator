#!/usr/bin/env python3
"""
检查环境变量加载情况的脚本
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 检查KIMI_API_KEY
kimi_key = os.getenv("KIMI_API_KEY")
print("=== 环境变量检查结果 ===")
print(f"KIMI_API_KEY: {kimi_key}")
print(f"密钥长度: {len(kimi_key) if kimi_key else 'None'}")

if kimi_key:
    print(f"密钥前缀: {kimi_key[:15]}...")
    print(f"密钥完整值: '{kimi_key}'")
    
    # 检查是否有额外空格
    print(f"密钥去除前后空格: '{kimi_key.strip()}'")
    print(f"原始长度 vs 清理后长度: {len(kimi_key)} vs {len(kimi_key.strip())}")