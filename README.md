# 实时字幕翻译工具 🎯

一个基于macOS的实时英文转中文字幕翻译工具，支持语音识别和实时翻译显示。

## 🚀 功能特性

- **实时语音识别**: 使用Whisper模型进行英文语音识别
- **智能翻译**: 使用OpenAI GPT进行高质量中文翻译
- **悬浮字幕**: 桌面悬浮窗显示翻译结果
- **低延迟**: 优化处理流程，延迟<500ms
- **可拖拽**: 字幕窗口支持鼠标拖拽定位
- **透明度调节**: 支持窗口透明度设置

## 📋 系统要求

- **系统**: macOS 10.15+
- **Python**: 3.8+
- **音频驱动**: BlackHole (推荐) 或 Soundflower
- **内存**: 至少4GB

## 🔧 安装步骤

### 1. 安装音频驱动

**推荐：安装BlackHole**
```bash
# 使用Homebrew安装
brew install blackhole-16ch

# 或从官网下载
# https://existential.audio/blackhole/
```

**配置音频路由**
1. 打开"音频MIDI设置"
2. 创建多输出设备
3. 添加BlackHole和你的扬声器
4. 设置默认输入为BlackHole

### 2. 安装Python依赖

```bash
cd realtime-subtitle-translator
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp env.example .env
# 编辑.env文件，填入你的API密钥
```

**重要：** `.env` 文件包含敏感信息，已被 `.gitignore` 排除，不会上传到Git仓库。

## 🎯 快速开始

```bash
# 启动程序
python main.py

# 测试音频捕获
python -m src.audio_capture

# 测试翻译功能
python -m src.translation
```

## ⚙️ 配置说明

编辑 `.env` 文件进行个性化配置：

```bash
# OpenAI配置
OPENAI_API_KEY=your_api_key_here

# Whisper配置
WHISPER_MODEL=base           # tiny/base/small/medium/large
WHISPER_DEVICE=cpu          # cpu/cuda

# 音频配置
SAMPLE_RATE=16000
CHUNK_SIZE=1024

# 显示配置
SUBTITLE_FONT_SIZE=24
SUBTITLE_FONT_COLOR=white
SUBTITLE_BG_COLOR=black
SUBTITLE_OPACITY=0.8
SUBTITLE_POSITION=bottom    # top/bottom/center

# 翻译配置
TARGET_LANGUAGE=zh-CN
TRANSLATION_DELAY_MS=500
MAX_SUBTITLE_LENGTH=50
```

## 🎮 使用指南

### 基本操作

1. **启动程序**: `python main.py`
2. **拖拽窗口**: 按住左键拖拽字幕窗口
3. **退出程序**: 按ESC键或Ctrl+C

### 快捷键

- `ESC`: 退出程序
- `Cmd+Shift+T`: 显示/隐藏字幕
- `Cmd+Shift+R`: 重新加载配置

### 高级用法

```python
# 自定义翻译
from src.translation import OpenAITranslator

async def custom_translate():
    translator = OpenAITranslator()
    result = await translator.translate("Hello, world!")
    print(result)  # 输出: 你好，世界！
```

## 🔍 故障排除

### 常见问题

**Q: 没有声音输入**
- 检查BlackHole是否正确安装
- 确认音频MIDI设置中BlackHole已启用
- 检查系统隐私设置中的麦克风权限

**Q: 翻译延迟很大**
- 降低Whisper模型大小（使用tiny/base）
- 检查网络连接质量
- 调整CHUNK_SIZE和BUFFER_DURATION参数

**Q: 字幕窗口不显示**
- 检查Python tkinter是否可用
- 尝试使用控制台模式: `export DISPLAY_MODE=console`

### 调试模式

```bash
# 启用详细日志
python main.py --debug

# 测试音频捕获
python -c "import sounddevice as sd; print(sd.query_devices())"
```

## 🛠️ 开发指南

### 项目结构

```
realtime-subtitle-translator/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── audio_capture.py     # 音频捕获模块
│   ├── transcription.py     # 语音识别模块
│   ├── translation.py       # 翻译模块
│   └── subtitle_overlay.py  # 字幕显示模块
├── tests/                   # 测试文件
├── config/                  # 配置文件
├── scripts/                 # 工具脚本
├── main.py                  # 主程序
├── requirements.txt         # 依赖列表
└── README.md               # 项目说明
```

### 添加新功能

1. **新的翻译引擎**: 继承 `BaseTranslator` 类
2. **新的显示方式**: 继承 `BaseOverlay` 类
3. **音频预处理**: 修改 `AudioCapture` 类

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_audio.py
```

## 📈 性能优化

### 降低延迟的技巧

1. **使用较小的Whisper模型**: tiny/base比large快10倍
2. **优化音频缓冲区**: 减少buffer_duration到2秒
3. **本地缓存**: 缓存常用短语的翻译结果
4. **并发处理**: 使用asyncio并行处理音频和翻译

### 资源使用

| 模型 | 内存占用 | 延迟 | 准确率 |
|------|----------|------|--------|
| tiny | ~200MB | 100ms | 80% |
| base | ~500MB | 200ms | 85% |
| small | ~1GB | 400ms | 90% |
| medium | ~2GB | 800ms | 93% |

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置

```bash
git clone https://github.com/your-username/realtime-subtitle-translator.git
cd realtime-subtitle-translator
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 代码规范

- 使用Black格式化代码
- 添加类型注解
- 编写单元测试
- 更新文档

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [OpenAI Whisper](https://github.com/openai/whisper) - 语音识别
- [Kimi AI](https://platform.moonshot.cn) - 翻译服务
- [BlackHole](https://existential.audio/blackhole/) - 音频驱动
- [SoundDevice](https://python-sounddevice.readthedocs.io/) - 音频处理

## 📞 联系方式

有问题或建议？请提交 [Issue](https://github.com/your-username/realtime-subtitle-translator/issues)