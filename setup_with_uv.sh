#!/bin/bash

# 实时字幕翻译工具安装脚本 (使用uv)
# macOS专用

set -e

echo "🎯 实时字幕翻译工具安装脚本 (使用uv)"
echo "==================================="

# 检查系统
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此脚本仅支持macOS"
    exit 1
fi

# 检查uv是否安装
if ! command -v uv &> /dev/null; then
    echo "📦 安装uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# 检查Python版本
if ! uv python find &> /dev/null; then
    echo "📦 安装Python 3.11..."
    uv python install 3.11
fi

# 创建虚拟环境
echo "🐍 创建uv虚拟环境..."
uv venv --python 3.11
source .venv/bin/activate

# 安装音频驱动
echo "🔊 安装BlackHole音频驱动..."
if command -v brew &> /dev/null; then
    if brew list blackhole-16ch &> /dev/null; then
        echo "✅ BlackHole已安装"
    else
        brew install blackhole-16ch
    fi
else
    echo "⚠️  未找到Homebrew，请先安装:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
fi

# 安装项目依赖
echo "📦 安装项目依赖..."
uv pip install -e "."

# 安装PyAudio依赖
echo "🔧 安装PyAudio..."
brew install portaudio
uv pip install pyaudio

# 下载Whisper模型
echo "🤖 下载Whisper模型..."
source .venv/bin/activate
python3 -c "
import whisper
print('下载基础模型...')
whisper.load_model('base')
print('下载完成')
"

# 创建启动脚本
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python main.py "$@"
EOF

chmod +x start.sh

# 创建uv启动脚本
cat > start_uv.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
uv run python main.py "$@"
EOF

chmod +x start_uv.sh

# 测试安装
echo "🧪 测试安装..."
source .venv/bin/activate
python3 -c "
import sounddevice as sd
print('✅ 音频设备检测:')
print(sd.query_devices())
"

echo ""
echo "🎉 uv环境安装完成！"
echo "=================="
echo "使用方法:"
echo "1. 编辑 .env 文件，填入OpenAI API密钥"
echo "2. 运行: ./start.sh 或 ./start_uv.sh"
echo "3. 或运行: uv run python main.py"
echo ""
echo "📖 查看 README.md 获取更多使用说明"