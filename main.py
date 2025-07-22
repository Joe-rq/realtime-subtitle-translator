#!/usr/bin/env python3
"""
实时字幕翻译工具主程序
"""
import asyncio
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Coroutine
import numpy as np
from dotenv import load_dotenv

from src.audio_capture import AudioCapture
from src.subtitle_overlay import SubtitleOverlay
from src.transcription import WhisperTranscriber
from src.translation import KimiTranslator

# 加载环境变量
load_dotenv(override=True)


# 配置日志
def setup_logging():
    """配置日志系统"""
    # 创建logs目录
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # 创建主日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # 转写结果日志处理器
    transcript_logger = logging.getLogger("transcript")
    transcript_logger.setLevel(logging.INFO)
    
    # 使用日期时间创建唯一的日志文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_file = logs_dir / f"transcript_{timestamp}.log"
    
    # 文件处理器
    file_handler = logging.FileHandler(transcript_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(file_format)
    transcript_logger.addHandler(file_handler)
    
    return logger, transcript_logger


class Application:
    """
    应用程序类，负责协调所有组件
    """

    def __init__(self, transcriber, translator, audio_capture, overlay, logger, transcript_logger):
        self.transcriber = transcriber
        self.translator = translator
        self.audio_capture = audio_capture
        self.overlay = overlay
        self.running = False
        self._main_task = None
        self.loop = asyncio.get_event_loop()
        self.logger = logger
        self.transcript_logger = transcript_logger

    async def _main_loop(self):
        """
        主处理循环
        """
        try:
            await self.audio_capture.start()
            self.logger.info("✅ 实时翻译服务已启动")

            while self.running:
                audio_data = await self.audio_capture.get_audio_chunk()
                audio_data = await self.audio_capture.get_audio_chunk()
                if audio_data is None:
                    await asyncio.sleep(0.01)
                    continue

                text = await self.transcriber.transcribe(audio_data)

                if not text:
                    await asyncio.sleep(0.01)
                    continue
                if not text or not text.strip():
                    continue
                
                # 记录识别结果到控制台和日志文件
                self.logger.info(f"🎤 识别: {text}")
                self.transcript_logger.info(f"[原文] {text}")

                translated = await self.translator.translate(text)
                if not translated:
                    continue
                
                # 记录翻译结果到控制台和日志文件
                self.logger.info(f"🌏 翻译: {translated}")
                self.transcript_logger.info(f"[翻译] {translated}")
                
                # 在日志中添加一个空行，使记录更清晰
                self.transcript_logger.info("")

                self.overlay.update_subtitle(translated)

        except asyncio.CancelledError:
            self.logger.info("🛑 主循环被取消")
        except Exception as e:
            self.logger.error(f"❌ 主循环出现错误: {e}")
        finally:
            self.logger.info("正在清理资源...")
            if self.audio_capture.is_running():
                await self.audio_capture.stop()
            self.overlay.hide()
            self.logger.info("✅ 清理完成")

    def _drive_async_loop(self):
        """驱动asyncio事件循环"""
        if self.running and self.overlay.root:
            self.loop.stop()
            self.loop.run_forever()
            # 使用 after 调度下一次执行，将控制权还给tkinter
            self.overlay.root.after(50, self._drive_async_loop)


    def start(self):
        """
        启动应用程序 - GUI在主线程，asyncio也在主线程
        """
        if self.running:
            self.logger.info("应用已在运行中")
            return

        self.running = True
        self.logger.info("🎯 启动实时字幕翻译工具...")

        # 先显示GUI，确保root已初始化
        self.overlay.show()
        
        # 确保GUI已就绪
        if not self.overlay.root:
            self.logger.error("❌ 无法初始化GUI")
            return

        # 创建asyncio任务
        self._main_task = self.loop.create_task(self._main_loop())

        # 启动asyncio事件循环的驱动器
        self.overlay.root.after(50, self._drive_async_loop)
        
        # 启动tkinter的GUI事件循环
        self.overlay.run_gui_loop()

        # GUI循环结束后，清理工作
        self.stop()


    def stop(self):
        """
        停止应用程序
        """
        if not self.running:
            return

        self.logger.info("🛑 正在停止服务...")
        self.running = False
        if self._main_task:
            self._main_task.cancel()
        
        # 确保loop停止
        if self.loop.is_running():
            self.loop.stop()
        
        # 关闭loop
        self.loop.close()
        self.logger.info("👋 程序已退出")
        sys.exit(0)



def main():
    """
    主函数
    """
    # 设置日志系统
    logger, transcript_logger = setup_logging()
    logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    transcript_logger.info(f"=== 实时字幕转写记录 - 会话开始于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    # 依赖注入：在这里创建和配置组件
    # 依赖注入：在这里创建和配置组件
    language = os.getenv("WHISPER_LANGUAGE", "auto")
    audio_capture = AudioCapture()
    transcriber = WhisperTranscriber(language=language)
    
    translator = KimiTranslator()
    
    overlay = SubtitleOverlay() # tkinker overlay 必须在主线程创建

    app = Application(
        transcriber=transcriber,
        translator=translator,
        audio_capture=audio_capture,
        overlay=overlay,
        logger=logger,
        transcript_logger=transcript_logger
    )

    def handle_signal(sig, frame):
        logger.info(f"\n📱 收到信号 {sig}，正在停止...")
        app.stop()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # 启动应用
    app.start()



if __name__ == "__main__":
    main()