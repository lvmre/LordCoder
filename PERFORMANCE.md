# LordCoder Performance Optimization Guide

This guide helps you get the best performance from LordCoder on your system.

## 🚀 Model Selection Guide

### Recommended Models for Your System

**Your Hardware**: Intel i5-10400 + 24GB RAM

| Model | RAM Usage | Speed | Best For |
|-------|-----------|-------|----------|
| `qwen2.5-coder:7b` | ~8GB | ⚡ Fast | Quick tasks, debugging |
| `qwen2.5-coder:14b` | ~14GB | 🚀 Balanced | General coding (recommended) |
| `qwen2.5-coder:32b` | ~20GB | 🐢 Slower | Complex tasks, large projects |

### Switching Models

**To change models**:

1. **Download the model**:
   ```bash
   ollama pull qwen2.5-coder:7b    # For speed
   ollama pull qwen2.5-coder:32b   # For power
   ```

2. **Update configuration** (edit `lordcoder.yml`):
   ```yaml
   model: ollama/qwen2.5-coder:7b   # Change to desired model
   ```

3. **Restart LordCoder**:
   ```bash
   aider --config lordcoder.yml
   ```

## ⚡ System Optimization

### Windows Performance Settings

1. **Set high performance mode**:
   - Windows Settings > Power & sleep > Additional power settings
   - Select "High performance" or "Ultimate performance"

2. **Close unnecessary applications**:
   - Web browsers (especially with many tabs)
   - Development tools not in use
   - Background applications

3. **Disable Windows Defender real-time protection** (temporarily):
   - Only during intensive coding sessions
   - Re-enable after completion

### RAM Optimization

**Monitor RAM usage**:
```python
from src.lordcoder.utils import get_memory_info
memory = get_memory_info()
print(f"Available RAM: {memory.available / (1024**3):.1f} GB")
print(f"Usage: {memory.percent}%")
```

**Free up RAM**:
- Restart Ollama service: `ollama serve`
- Close other AI tools or chatbots
- Use smaller model if RAM < 16GB available

## 🔄 Workflow Optimization

### Efficient Prompting

1. **Be specific** in your requests
2. **Break large tasks** into smaller steps
3. **Provide context** about your project structure
4. **Use file references** when possible

### Batch Operations

**For multiple file changes**:
```
Please update all Python files to use f-strings instead of .format()
```

**For repetitive tasks**:
```
Create a template for new API endpoints following the existing pattern
```

### Caching Benefits

LordCoder remembers:
- Previous conversations in the session
- File changes made during the session
- Project structure and context

**Keep sessions open** for related tasks to benefit from caching.

## 🖥️ Hardware-Specific Tips

### Intel i5-10400 Optimization

1. **CPU cores**: Your CPU has 6 cores/12 threads
2. **Optimal usage**: LordCoder uses 1-2 cores effectively
3. **Temperature monitoring**: Keep CPU temp < 80°C

**Monitoring tools**:
- Task Manager > Performance tab
- HWMonitor for detailed stats
- Core Temp for CPU temperature

### RAM Management (24GB)

**Recommended allocation**:
- Operating system: ~4GB
- Ollama + model: 8-20GB (depending on model)
- Other applications: ~4GB
- **Free buffer**: ~4GB minimum

**RAM usage tips**:
- Use 14B model for balanced performance
- Upgrade to 32B only when needed
- Close browser tabs when using 32B model

## 📊 Performance Monitoring

### Built-in Monitoring

**Check system resources**:
```bash
python src/lordcoder/utils.py
```

**Monitor during use**:
- Task Manager for CPU/RAM usage
- Ollama logs for model loading times

### Performance Benchmarks

**Expected response times** (on your hardware):

| Model | Simple Query | Complex Task | Large File Analysis |
|-------|--------------|--------------|-------------------|
| 7B | 2-5 seconds | 10-20 seconds | 30-60 seconds |
| 14B | 3-8 seconds | 15-30 seconds | 45-90 seconds |
| 32B | 5-15 seconds | 30-60 seconds | 90-180 seconds |

## 🛠️ Advanced Optimization

### Ollama Configuration

**Set Ollama environment variables**:
```powershell
$env:OLLAMA_MAX_LOADED_MODELS = "1"
$env:OLLAMA_NUM_PARALLEL = "1"
$env:OLLAMA_MAX_QUEUE = "512"
```

**GPU acceleration** (if you add a GPU later):
```powershell
$env:OLLAMA_GPU = "1"
```

### Network Optimization

**For faster model downloads**:
- Use wired internet connection
- Download during off-peak hours
- Consider using a VPN if downloads are slow

### Storage Optimization

**SSD vs HDD**:
- Models load 2-3x faster on SSD
- Consider moving Ollama models to SSD:
  ```powershell
  $env:OLLAMA_MODELS = "D:\OllamaModels"
  ```

## 🔧 Troubleshooting Performance Issues

### Slow Response Times

**Symptoms**: Responses take >30 seconds

**Solutions**:
1. Switch to smaller model (7B)
2. Restart Ollama service
3. Close other applications
4. Check for Windows updates

### High CPU Usage

**Symptoms**: CPU usage >80% for extended periods

**Solutions**:
1. Use smaller model
2. Check for background processes
3. Restart your computer
4. Monitor CPU temperature

### Memory Issues

**Symptoms**: System becomes sluggish, errors about memory

**Solutions**:
1. Use 7B model
2. Increase virtual memory
3. Restart Ollama to clear cache
4. Add more RAM if consistently low

## 📈 Performance Tips Summary

### Quick Wins
1. **Use 14B model** for balanced performance
2. **Close browser tabs** during intensive sessions
3. **Restart Ollama** if performance degrades
4. **Monitor RAM usage** before starting large tasks

### Advanced Users
1. **Environment variables** for fine-tuning
2. **SSD storage** for faster model loading
3. **Temperature monitoring** for sustained use
4. **Batch operations** for efficiency

### When to Upgrade Models
- **Stay with 7B**: Quick debugging, simple tasks
- **Move to 14B**: Most development work (recommended)
- **Upgrade to 32B**: Complex architecture, large refactoring

---

**Remember**: The 14B model provides the best balance of speed and capability for your i5-10400 + 24GB RAM setup. Start there and adjust based on your specific needs.
