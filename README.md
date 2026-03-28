# LordCoder

🚀 **LordCoder** is a powerful local AI coding assistant that brings world-class software engineering capabilities to your development environment. Built with Aider and Ollama, LordCoder provides intelligent multi-file editing, automated testing, and seamless git integration - all running locally on your machine for maximum privacy and speed.

## ✨ Features

- **🧠 Intelligent Multi-File Editing**: Make coordinated changes across your entire codebase
- **🔧 Automated Testing**: Automatically runs pytest after code changes
- **📝 Smart Git Integration**: Auto-commits with meaningful messages
- **🎯 Step-by-Step Planning**: Methodical approach to complex tasks
- **🐍 Python Excellence**: Clean code with type hints, docstrings, and error handling
- **🔒 Complete Privacy**: Runs entirely locally with Ollama
- **⚡ Fast Performance**: Optimized for modern hardware (24GB RAM recommended)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher (3.13 supported with uv installation)
- 24GB RAM (for qwen2.5-coder:14b model)
- Windows 10/11
- Ollama installed

### Installation

**Method 1: Automatic Setup (Recommended)**
```bash
# Run the enhanced setup script
install.bat
```

**Method 2: Manual Setup with uv**
```bash
# Install uv (Python package manager)
pip install uv

# Install aider-chat with Python 3.12 compatibility
python -m uv tool install --force --python python3.12 aider-chat

# Setup PATH for uv tools
$env:PATH = "C:\Users\lovem\.local\bin;$env:PATH"

# Download AI model
ollama pull qwen2.5-coder:14b
```

**Method 3: Traditional Setup**
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install aider-chat==0.13.0 psutil pytest pytest-cov

# Install Ollama from https://ollama.com
ollama pull qwen2.5-coder:14b
```

### Launch LordCoder

```bash
# Method 1: uv-based (recommended)
aider --config lordcoder.yml

# Method 2: uv tool run
python -m uv tool run aider --config lordcoder.yml

# Method 3: virtual environment
.venv\Scripts\activate
aider --config lordcoder.yml
```

## 💡 Usage Examples

### Create a New Project
```
Create a Python package with utils for system monitoring, include tests and documentation
```

### Debug Existing Code
```
Fix the failing tests in the authentication module, add proper error handling
```

### Refactor Codebase
```
Refactor the data processing pipeline to use async/await, update all related files
```

## 🏗️ Project Structure

```
LordCoder/
├── lordcoder.yml          # Main configuration
├── requirements.txt        # Python dependencies
├── install.bat           # One-click setup script
├── src/lordcoder/        # Package directory
├── tests/                # Test suite
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🎯 LordCoder Personality

LordCoder is designed as a senior software engineer with these characteristics:

- **Methodical Planning**: Always thinks step-by-step before coding
- **Code Quality**: Writes clean, modern Python with full type hints
- **Testing First**: Automatically suggests and runs relevant tests
- **Git Best Practices**: Creates feature branches and writes clear commit messages
- **Autonomous**: Proactively handles full project building while staying safe

## 🔧 Configuration

The `lordcoder.yml` file contains the core configuration:

- **Model**: `ollama/qwen2.5-coder:32b` - Optimized for 24GB RAM systems
- **Auto-commits**: Enabled for seamless workflow
- **Testing**: Integrated with pytest
- **Git**: Full integration with version control

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 16GB | 24GB |
| CPU | 4 cores | 6+ cores |
| Python | 3.8 | 3.11+ |
| Storage | 10GB | 20GB |

## � Documentation

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[PERFORMANCE.md](PERFORMANCE.md)** - Optimization tips and model selection
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## �🐛 Troubleshooting

### Common Issues

**"Out of memory" error:**
- Try a smaller model: `ollama pull qwen2.5-coder:7b`
- Update `lordcoder.yml` to use the smaller model

**"Ollama not found":**
- Make sure Ollama is installed and running
- Try `ollama serve` in a separate terminal

**"Module not found" errors:**
- Activate virtual environment: `.venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Getting Help

1. Check the [Issues](https://github.com/lvmre/LordCoder/issues) page
2. Review the troubleshooting section above
3. Create a new issue with your system details

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Aider](https://github.com/paul-gauthier/aider) - The amazing AI pair programming tool
- [Ollama](https://ollama.com) - Local AI model runtime
- [Qwen2.5-Coder](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct) - Powerful coding model

## 📞 Contact

Built with ❤️ by [Lovemore](https://github.com/lvmre) in Johannesburg

---

**LordCoder: Your local AI coding companion for building amazing software, faster and privately.**