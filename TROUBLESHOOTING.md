# LordCoder Troubleshooting Guide

This guide helps you resolve common issues with LordCoder setup and operation.

## 🔧 Installation Issues

### Python Version Compatibility

**Problem**: `aider-chat` installation fails with Python version errors
```
ERROR: No matching distribution found for aider-chat>=0.35.0
```

**Solutions**:
1. **Use uv installation (Recommended)**:
   ```bash
   pip install uv
   python -m uv tool install --force --python python3.12 aider-chat
   ```

2. **Use Python 3.12 virtual environment**:
   ```bash
   python3.12 -m venv .venv
   .venv\Scripts\activate
   pip install aider-chat==0.13.0
   ```

3. **Run the enhanced install script**:
   ```bash
   install.bat
   ```

### 'aider' Command Not Found

**Problem**: `aider: command not found` after installation

**Solutions**:
1. **Add uv tools to PATH**:
   ```powershell
   $env:PATH = "C:\Users\lovem\.local\bin;$env:PATH"
   ```

2. **Restart your terminal** after uv installation

3. **Use uv tool run directly**:
   ```bash
   python -m uv tool run aider --config lordcoder.yml
   ```

### Ollama Issues

**Problem**: Ollama not found or connection failed

**Solutions**:
1. **Install Ollama** from https://ollama.com

2. **Start Ollama service**:
   ```bash
   ollama serve
   ```

3. **Check Ollama status**:
   ```bash
   ollama --version
   ollama list
   ```

## 🚀 Model Performance Issues

### Slow Response Times

**Problem**: AI responses are slow on your system

**Solutions**:
1. **Use smaller model**:
   ```bash
   ollama pull qwen2.5-coder:7b
   # Edit lordcoder.yml to use model: ollama/qwen2.5-coder:7b
   ```

2. **Close unnecessary applications** to free RAM

3. **Restart Ollama service**:
   ```bash
   # Stop Ollama, then restart
   ollama serve
   ```

### Model Download Failures

**Problem**: `ollama pull` fails or is very slow

**Solutions**:
1. **Check internet connection**

2. **Use smaller model first**:
   ```bash
   ollama pull qwen2.5-coder:7b
   ```

3. **Retry download** (sometimes servers are busy)

4. **Check available disk space** (models need several GB)

## 🐛 Runtime Issues

### Git Integration Problems

**Problem**: Auto-commits not working

**Solutions**:
1. **Initialize git repository**:
   ```bash
   git init
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

2. **Check git status**:
   ```bash
   git status
   ```

3. **Disable auto-commits temporarily** (in lordcoder.yml):
   ```yaml
   auto-commits: false
   ```

### Test Failures

**Problem**: Pytest tests fail after code changes

**Solutions**:
1. **Install test dependencies**:
   ```bash
   pip install pytest pytest-cov
   ```

2. **Run tests manually**:
   ```bash
   pytest tests/ -v
   ```

3. **Check Python path**:
   ```bash
   python -c "import sys; print(sys.path)"
   ```

### Windows Path Issues

**Problem**: File path errors on Windows

**Solutions**:
1. **Use raw strings for paths** in Python code:
   ```python
   path = r"C:\Users\name\file.txt"
   ```

2. **Use pathlib** for cross-platform compatibility:
   ```python
   from pathlib import Path
   path = Path("C:/Users/name/file.txt")
   ```

3. **Escape backslashes** in configurations:
   ```yaml
   path: "C:\\Users\\name\\file.txt"
   ```

## 📊 System Resource Issues

### Out of Memory Errors

**Problem**: System runs out of RAM when using large models

**Solutions**:
1. **Use smaller model**: qwen2.5-coder:7b instead of :14b or :32b

2. **Close other applications** to free RAM

3. **Restart Ollama** to clear cached models

4. **Monitor system resources**:
   ```python
   from src.lordcoder.utils import get_memory_info
   memory = get_memory_info()
   print(f"Memory usage: {memory.percent}%")
   ```

### CPU Usage Too High

**Problem**: System becomes unresponsive during AI processing

**Solutions**:
1. **Use smaller model** for faster processing

2. **Set lower CPU priority** for Ollama process

3. **Take breaks** between complex requests

## 🔍 Debugging Steps

### General Troubleshooting

1. **Check all components**:
   ```bash
   python --version
   python -m uv --version
   aider --version
   ollama --version
   ```

2. **Test configuration**:
   ```bash
   aider --config lordcoder.yml --version
   ```

3. **Run with verbose output**:
   ```bash
   aider --config lordcoder.yml --verbose
   ```

### Log Collection

**To get help with issues, collect this information**:

1. **System information**:
   ```bash
   python src/lordcoder/utils.py
   ```

2. **Installation details**:
   ```bash
   pip list | findstr aider
   pip list | findstr uv
   pip list | findstr ollama
   ```

3. **Error messages** (full output, not just last line)

## 📞 Getting Help

### Self-Service Resources

1. **Check this guide** for common solutions
2. **Review README.md** for setup instructions
3. **Search GitHub Issues** for similar problems

### Creating Support Requests

If you need additional help, provide:

1. **System information**:
   - Windows version
   - Python version
   - Available RAM
   - Error messages

2. **What you tried**:
   - Installation method used
   - Commands run
   - Output received

3. **Expected vs actual behavior**

### Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| `aider` not found | `python -m uv tool run aider --config lordcoder.yml` |
| Python version error | Use uv installation method |
| Slow performance | Use qwen2.5-coder:7b model |
| Ollama not working | Install from ollama.com and run `ollama serve` |
| Git issues | Run `git init` and configure user info |
| Path errors | Use raw strings or pathlib in Python |

---

**Remember**: LordCoder is designed to be robust. Most issues are resolved by using the uv installation method and ensuring Ollama is running properly.
