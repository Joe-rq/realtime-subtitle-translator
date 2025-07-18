#!/bin/bash

# 实时字幕翻译工具安装脚本
# macOS专用

set -e

echo "🎯 实时字幕翻译工具安装脚本"
echo "=================================="

# 检查系统
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此脚本仅支持macOS"
    exit 1
fi

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3.8+"
    echo "访问: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python版本: $PYTHON_VERSION"

# 检查Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 安装Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 安装音频驱动
echo "🔊 安装BlackHole音频驱动..."
if brew list blackhole-16ch &> /dev/null; then
    echo "✅ BlackHole已安装"
else
    brew install blackhole-16ch
fi

# 创建Python虚拟环境
echo "🐍 创建Python虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 检查并安装PyAudio依赖
echo "🔧 安装PyAudio依赖..."
brew install portaudio
pip install pyaudio

# 下载Whisper模型
echo "🤖 下载Whisper模型..."
python3 -c "
import whisper
print('下载基础模型...')
whisper.load_model('base')
print('下载完成')
"

# 配置音频设置
echo "🎵 配置音频设置..."
cat << EOF

🎼 音频配置步骤：
1. 打开"音频MIDI设置"（在应用程序>实用工具中）
2. 点击左下角"+"，创建"多输出设备"
3. 勾选"BlackHole 16ch"和你的扬声器
4. 将此多输出设备设为系统默认输出
5. 在系统设置>声音>输入中，选择"BlackHole 16ch"作为输入

📱 使用方法：
1. 编辑.env文件，填入OpenAI API密钥
2. 运行: python main.py
3. 拖拽字幕窗口到合适位置
4. 按ESC退出

EOF

# 创建快捷启动脚本
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py "$@"
EOF

chmod +x start.sh

# 测试安装
echo "🧪 测试安装..."
source venv/bin/activate
python3 -c "
import sounddevice as sd
print('✅ 音频设备检测:')
print(sd.query_devices())
"

echo ""
echo "🎉 安装完成！"
echo "=============="
echo "1. 编辑 .env 文件，填入你的OpenAI API密钥"
echo "2. 运行: ./start.sh"
echo "3. 或运行: python main.py"
echo ""
echo "📖 查看 README.md 获取更多使用说明"