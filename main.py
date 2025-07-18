#!/usr/bin/env python3
"""
实时字幕翻译工具主程序
"""
import asyncio
import signal
import sys
import threading
import time
from pathlib import Path

from src.audio_capture import AudioCapture
from src.transcription import WhisperTranscriber
from src.translation import KimiTranslator
from src.subtitle_overlay import SubtitleOverlay

class RealtimeTranslator:
    def __init__(self):
        self.running = False
        self.audio_capture = None
        self.transcriber = None
        self.translator = None
        self.overlay = None
        self.processing_thread = None

    def start(self):
        """启动实时翻译服务 - 在主线程中运行GUI"""
        print("🎯 启动实时字幕翻译工具...")
        
        try:
            # 初始化各个模块
            self.audio_capture = AudioCapture()
            self.transcriber = WhisperTranscriber()
            self.translator = KimiTranslator()
            self.overlay = SubtitleOverlay()
            
            # 在主线程启动字幕显示
            self.overlay.show()
            
            self.running = True
            print("✅ 实时翻译服务已启动")
            
            # 启动后台处理线程
            self.processing_thread = threading.Thread(
                target=self._run_async_processing, 
                daemon=True
            )
            self.processing_thread.start()
            
            # 在主线程运行GUI循环
            self.overlay.run_gui_loop()
            
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            self.stop()
            sys.exit(1)

    def _run_async_processing(self):
        """在后台线程中运行异步处理逻辑"""
        asyncio.run(self._async_main_loop())

    async def _async_main_loop(self):
        """异步主处理循环"""
        try:
            # 启动音频捕获
            await self.audio_capture.start()
            
            while self.running:
                try:
                    # 获取音频数据
                    audio_data = await self.audio_capture.get_audio_chunk()
                    
                    if audio_data is None:
                        await asyncio.sleep(0.1)
                        continue
                    
                    # 语音识别
                    text = await self.transcriber.transcribe(audio_data)
                    
                    if text and text.strip():
                        print(f"🎤 识别: {text}")
                        
                        # 翻译
                        translated = await self.translator.translate(text)
                        
                        if translated:
                            print(f"🌏 翻译: {translated}")
                            
                            # 显示字幕（线程安全）
                            self.overlay.update_subtitle(translated)
                    
                except Exception as e:
                    print(f"处理错误: {e}")
                    await asyncio.sleep(0.1)
                    
        except Exception as e:
            print(f"异步处理循环错误: {e}")

    def stop(self):
        """停止服务"""
        print("🛑 正在停止服务...")
        self.running = False
        
        # 停止各个组件
        if self.audio_capture:
            asyncio.create_task(self.audio_capture.stop())
        if self.overlay:
            self.overlay.hide()
            
        print("✅ 服务已停止")

    def handle_signal(self, signum, frame):
        """处理中断信号"""
        print(f"\n📱 收到信号 {signum}，正在停止...")
        self.stop()

def main():
    """主函数 - 在主线程运行"""
    translator = RealtimeTranslator()
    
    # 设置信号处理
    signal.signal(signal.SIGINT, translator.handle_signal)
    signal.signal(signal.SIGTERM, translator.handle_signal)
    
    # 启动服务（在主线程运行GUI）
    translator.start()

if __name__ == "__main__":
    main()