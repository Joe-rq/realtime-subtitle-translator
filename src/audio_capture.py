"""
音频捕获模块
使用macOS系统音频捕获
"""
import asyncio
import numpy as np
import sounddevice as sd
from typing import Optional
import logging
import queue
import threading

logger = logging.getLogger(__name__)

class AudioCapture:
    """音频捕获类"""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.stream = None
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.buffer_size = 10  # 缓冲区大小
        
    def is_running(self) -> bool:
        """检查音频捕获是否正在运行"""
        return self.is_recording

    async def start(self):
        """启动音频捕获"""
        try:
            # 获取可用设备
            devices = sd.query_devices()
            input_device = None
            
            # 查找BlackHole或系统音频捕获设备
            for i, device in enumerate(devices):
                if 'BlackHole' in device['name'] or 'Soundflower' in device['name']:
                    input_device = i
                    logger.info(f"使用音频设备: {device['name']}")
                    break
            
            if input_device is None:
                # 使用默认输入设备
                input_device = sd.default.device[0]
                logger.warning("未找到BlackHole，使用默认输入设备")
            
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                device=input_device,
                callback=self._audio_callback,
                blocksize=self.chunk_size,
                dtype=np.float32
            )
            
            self.stream.start()
            self.is_recording = True
            logger.info("音频捕获已启动")
            
        except Exception as e:
            logger.error(f"启动音频捕获失败: {e}")
            raise
    
    def _audio_callback(self, indata, frames, time, status):
        """音频数据回调"""
        if status:
            logger.warning(f"音频状态: {status}")
        
        if self.is_recording:
            try:
                # 将音频数据复制到队列中
                audio_data = indata.copy().flatten()
                
                # 如果队列太满，丢弃旧数据
                # 如果队列已满，丢弃最旧的数据以腾出空间
                if self.audio_queue.full():
                    self.audio_queue.get_nowait()  # 丢弃旧数据
                self.audio_queue.put_nowait(audio_data)
                
            except Exception as e:
                logger.error(f"音频回调错误: {e}")
    
    async def get_audio_chunk(self) -> Optional[np.ndarray]:
        """获取音频数据块"""
        if not self.is_recording:
            return None
        
        try:
            # 非阻塞获取音频数据
            data = self.audio_queue.get_nowait()
            if data is not None and isinstance(data, np.ndarray) and data.size > 0:
                return data
            return None
            
        except queue.Empty:
            return None
        except Exception as e:
            logger.error(f"读取音频数据失败: {e}")
            return None
    
    async def stop(self):
        """停止音频捕获"""
        self.is_recording = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            
        # 清空队列
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
                
        logger.info("音频捕获已停止")

    def get_audio_level(self) -> float:
        """获取当前音频电平"""
        try:
            data = self.audio_queue.get_nowait()
            return float(np.abs(data).mean())
        except queue.Empty:
            return 0.0
        except Exception:
            return 0.0