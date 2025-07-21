"""
翻译模块
使用Kimi API进行实时翻译
"""
import asyncio
import aiohttp
import json
import os
from typing import Optional
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class KimiTranslator:
    """Kimi翻译类"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv("KIMI_API_KEY")
        self.base_url = base_url or os.getenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
        self.target_language = os.getenv("TARGET_LANGUAGE", "zh-CN")
        self.session = None
        
        if not self.api_key:
            raise ValueError("未设置KIMI_API_KEY环境变量")
    
    async def __aenter__(self):
        """异步上下文管理器进入"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self.session:
            await self.session.close()
    
    async def translate(self, text: str) -> Optional[str]:
        """
        翻译文本
        
        Args:
            text: 要翻译的英文文本
            
        Returns:
            中文翻译文本或None
        """
        if not text or not text.strip():
            return None
        
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # 构建翻译提示
            messages = [
                {
                    "role": "system",
                    "content": f"你是一个专业的翻译助手，请将英文翻译成{self._get_language_name(self.target_language)}。要求翻译准确、自然，保留原意。"
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
            
            # 设置请求参数 - 使用Kimi模型
            payload = {
                "model": "moonshot-v1-8k",  # Kimi模型
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.3,
                "stream": False
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 发送翻译请求
            async with self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                response_text = await response.text()
                if response.status == 200:
                    logger.info(f"翻译API请求成功: {response.status}")
                else:
                    logger.error(f"API请求失败: {response.status}, 响应内容: {response_text[:200]}...")
                    logger.error(f"请求URL: {self.base_url}/chat/completions")
                    logger.error(f"请求头Authorization: Bearer {self.api_key[:15]}...")
                
                if response.status != 200:
                    return None
                
                data = await response.json()
                translated_text = data["choices"][0]["message"]["content"].strip()
                
                return translated_text
                
        except asyncio.TimeoutError:
            logger.error("翻译请求超时")
            return None
        except Exception as e:
            logger.error(f"翻译失败: {e}")
            return None
    
    async def translate_batch(self, texts: list[str]) -> list[Optional[str]]:
        """
        批量翻译文本
        
        Args:
            texts: 要翻译的文本列表
            
        Returns:
            翻译结果列表
        """
        tasks = [self.translate(text) for text in texts if text and text.strip()]
        return await asyncio.gather(*tasks)
    
    def _get_language_name(self, lang_code: str) -> str:
        """获取语言名称"""
        language_map = {
            "zh-CN": "简体中文",
            "zh-TW": "繁体中文",
            "ja": "日语",
            "ko": "韩语",
            "fr": "法语",
            "de": "德语",
            "es": "西班牙语",
            "ru": "俄语"
        }
        return language_map.get(lang_code, lang_code)
    
    async def test_connection(self) -> bool:
        """测试API连接"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with self.session.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                return response.status == 200
                
        except Exception as e:
            logger.error(f"连接测试失败: {e}")
            return False

class SimpleTranslator:
    """简单翻译类，用于演示和测试"""
    
    def __init__(self):
        self.translation_map = {
            "hello": "你好",
            "world": "世界",
            "good morning": "早上好",
            "thank you": "谢谢",
            "goodbye": "再见",
            "how are you": "你好吗",
            "i love you": "我爱你",
            "what is your name": "你叫什么名字",
            "nice to meet you": "很高兴见到你",
            "have a nice day": "祝你有美好的一天"
        }
    
    async def translate(self, text: str) -> Optional[str]:
        """简单翻译实现"""
        if not text or not text.strip():
            return None
        
        text_lower = text.lower().strip()
        
        # 简单映射翻译
        for key, value in self.translation_map.items():
            if key in text_lower:
                return value
        
        # 返回原始文本作为占位符
        return f"[翻译: {text}]"
    
    async def translate_batch(self, texts: list[str]) -> list[Optional[str]]:
        """批量翻译"""
        return [await self.translate(text) for text in texts]
    
    async def test_connection(self) -> bool:
        """测试连接"""
        return True