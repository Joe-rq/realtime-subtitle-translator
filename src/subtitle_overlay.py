"""
字幕渲染模块
创建桌面悬浮字幕显示
"""
import tkinter as tk
from tkinter import font as tkfont
import threading
import queue
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SubtitleOverlay:
    """字幕悬浮窗类"""
    
    def __init__(self):
        self.root = None
        self.label = None
        self.current_text = ""
        self.running = False
        self.gui_ready = False
        
        # 配置参数
        self.font_size = int(os.getenv("SUBTITLE_FONT_SIZE", 24))
        self.font_color = os.getenv("SUBTITLE_FONT_COLOR", "white")
        self.bg_color = os.getenv("SUBTITLE_BG_COLOR", "black")
        self.opacity = float(os.getenv("SUBTITLE_OPACITY", 0.8))
        self.position = os.getenv("SUBTITLE_POSITION", "bottom")
        
    def show(self):
        """显示字幕悬浮窗 - 必须在主线程调用"""
        if self.running:
            return
            
        self.running = True
        self._create_window()
        
    def _create_window(self):
        """创建悬浮窗口 - 在主线程中运行"""
        try:
            self.root = tk.Tk()
            self.root.title("实时字幕翻译")
            
            # 设置窗口属性
            self.root.overrideredirect(True)  # 无边框
            self.root.attributes('-topmost', True)  # 置顶
            self.root.attributes('-alpha', self.opacity)  # 透明度
            
            # 设置窗口大小和位置
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            window_width = 800
            window_height = 100
            
            if self.position == "bottom":
                x = (screen_width - window_width) // 2
                y = screen_height - window_height - 50
            elif self.position == "top":
                x = (screen_width - window_width) // 2
                y = 50
            else:  # center
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
            
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # 创建标签
            self.label = tk.Label(
                self.root,
                text="准备就绪...",
                font=tkfont.Font(family="PingFang SC", size=self.font_size),
                fg=self.font_color,
                bg=self.bg_color,
                wraplength=window_width - 40,
                justify="center",
                pady=20
            )
            self.label.pack(fill=tk.BOTH, expand=True)
            
            # 绑定事件
            self.root.bind('<Button-1>', self._start_move)
            self.root.bind('<ButtonRelease-1>', self._stop_move)
            self.root.bind('<B1-Motion>', self._on_move)
            self.root.bind('<Escape>', lambda e: self.hide())
            
            # 标记GUI就绪
            self.gui_ready = True
            
        except Exception as e:
            logger.error(f"创建悬浮窗失败: {e}")
            self.running = False
    
    def _start_move(self, event):
        """开始拖动窗口"""
        self.x = event.x
        self.y = event.y
    
    def _stop_move(self, event):
        """停止拖动窗口"""
        self.x = None
        self.y = None
    
    def _on_move(self, event):
        """窗口拖动"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def update_subtitle(self, text: str):
        """更新字幕内容 - 在单线程模型下是安全的"""
        if text and self.running and self.label and text != self.current_text:
            self.current_text = text
            self.label.config(text=text)
    
    def hide(self):
        """隐藏字幕悬浮窗"""
        if not self.running:
            return
            
        self.running = False
        
        if self.root:
            self.root.destroy()
            self.root = None
            
        self.gui_ready = False
    
    def run_gui_loop(self):
        """运行GUI主循环 - 必须在主线程调用"""
        if self.root:
            self.root.mainloop()
    
    def set_position(self, x: int, y: int):
        """设置悬浮窗位置"""
        if self.root:
            self.root.geometry(f"+{x}+{y}")
    
    def set_opacity(self, opacity: float):
        """设置透明度"""
        self.opacity = max(0.1, min(1.0, opacity))
        if self.root:
            self.root.attributes('-alpha', self.opacity)
    
    def set_font_size(self, size: int):
        """设置字体大小"""
        self.font_size = max(8, min(48, size))
        if self.label:
            self.label.config(font=tkfont.Font(family="PingFang SC", size=self.font_size))

class SimpleConsoleOverlay:
    """简单的控制台字幕显示（备用方案）"""
    
    def __init__(self):
        self.current_text = ""
        self.running = False
    
    def show(self):
        """显示字幕"""
        self.running = True
        print("📝 字幕显示已启动（控制台模式）")
    
    def hide(self):
        """隐藏字幕"""
        self.running = False
        print("📝 字幕显示已停止")
    
    def update_subtitle(self, text: str):
        """更新字幕"""
        if text and text != self.current_text:
            self.current_text = text
            print(f"💬 {text}")
    
    def run_gui_loop(self):
        """空实现，保持接口一致"""
        pass
    
    def set_opacity(self, opacity: float):
        """设置透明度（控制台模式无效）"""
        pass
    
    def set_font_size(self, size: int):
        """设置字体大小（控制台模式无效）"""
        pass
    
    def set_position(self, x: int, y: int):
        """设置位置（控制台模式无效）"""
        pass