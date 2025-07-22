"""
语音识别模块
使用Faster-Whisper进行实时语音识别
"""
import asyncio
import tempfile
import numpy as np
from faster_whisper import WhisperModel
from typing import Optional
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class WhisperTranscriber:
    """Faster-Whisper语音识别类"""
    
    def __init__(self, model_name: str = "base", device: str = "cpu", language: str = "auto"):
        self.model_name = model_name
        self.device = device
        self.language = language
        self.model = None
        self.audio_buffer = np.array([], dtype=np.float32)
        self.buffer_duration = 5.0  # 缓冲区持续时间（秒）
        self.sample_rate = 16000
        
    async def load_model(self):
        """加载Whisper模型"""
        try:
            logger.info(f"正在加载Faster-Whisper模型: {self.model_name}")
            
            # Faster-Whisper支持CPU和CUDA
            device = "cpu"  # 在macOS上使用CPU
            
            self.model = WhisperModel(
                self.model_name,
                device=device,
                compute_type="int8"  # 使用int8量化提高速度
            )
            
            logger.info(f"模型加载完成，使用设备: {device}")
            
        except Exception as e:
            logger.error(f"加载模型失败: {e}")
            raise
    
    async def transcribe(self, audio_data: np.ndarray) -> Optional[str]:
        """
        转录音频数据
        
        Args:
            audio_data: 音频数据 (numpy array)
            
        Returns:
            转录文本或None
        """
        if self.model is None:
            await self.load_model()
        
        if audio_data is None or (isinstance(audio_data, np.ndarray) and audio_data.size == 0):
            return None
        
        try:
            # 累积音频数据到缓冲区
            self.audio_buffer = np.concatenate([self.audio_buffer, audio_data])
            
            # 检查缓冲区是否足够
            required_samples = int(16000 * self.buffer_duration)  # 3秒音频
            if len(self.audio_buffer) < required_samples:
                return None
            
            # 获取完整的音频数据块
            audio_chunk = np.array(self.audio_buffer)
            self.audio_buffer = np.array([], dtype=np.float32) # 清空缓冲区

            # 直接在内存中处理音频
            segments, info = self.model.transcribe(
                audio_chunk,
                language=self.language if self.language != "auto" else None,
                task="transcribe",
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )

            text_parts = [segment.text.strip() for segment in segments]
            text = " ".join(text_parts).strip()

            if text and len(text) > 1:  # 过滤掉非常短的文本
                logger.info(f"识别结果: '{text}' (语言: {info.language}, 置信度: {info.language_probability:.2f})")
                return text

            return None
                
        except Exception as e:
            logger.error(f"转录失败: {e}")
            return None
    
    def clear_buffer(self):
        """清空音频缓冲区"""
        self.audio_buffer = np.array([], dtype=np.float32)
    
    def get_buffer_info(self) -> dict:
        """获取缓冲区信息"""
        return {
            "buffer_size": len(self.audio_buffer),
            "buffer_duration": len(self.audio_buffer) / 16000,
            "model_loaded": self.model is not None
        }