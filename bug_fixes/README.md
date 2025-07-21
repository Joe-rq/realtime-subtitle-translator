# Bug修复调试脚本

此文件夹包含了用于诊断和修复实时字幕翻译工具中API密钥认证问题的调试脚本。

## 文件说明

### 环境检查脚本
- `check_env.py` - 检查环境变量是否正确加载
- `check_main_env.py` - 检查main.py中的环境变量加载情况

### API测试脚本
- `test_api.py` - 测试Kimi API连接
- `test_translation.py` - 测试翻译功能
- `verify_key.py` - 验证API密钥有效性

### 调试脚本
- `debug_api.py` - 调试API调用问题
- `debug_key.py` - 调试API密钥相关问题
- `debug_main.py` - 调试主程序环境

## 修复的Bug

**问题**: 程序运行时显示401认证错误，尽管API密钥在独立测试中有效

**根因**: 环境变量加载顺序问题，`load_dotenv()`没有正确覆盖已存在的环境变量

**解决方案**: 
- 修改`main.py`中的`load_dotenv()`调用为`load_dotenv(override=True)`
- 确保从`.env`文件正确加载实际API密钥

## 使用方法

这些脚本主要用于调试目的，如果需要重新验证系统：

```bash
# 检查API密钥有效性
python bug_fixes/verify_key.py

# 测试翻译功能
python bug_fixes/test_translation.py

# 检查环境变量
python bug_fixes/check_env.py
```