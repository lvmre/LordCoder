@echo off
echo ========================================
echo      LordCoder AI (Python 3.12)
echo ========================================
echo.

:: Check Python 3.12
python3.12 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.12 not found
    echo Run install-aider-312.bat first
    pause
    exit /b 1
)

:: Check Ollama
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama not found
    echo Install from: https://ollama.com
    pause
    exit /b 1
)

:: Check AI model
ollama list | findstr "qwen2.5-coder" >nul 2>&1
if errorlevel 1 (
    echo Downloading qwen2.5-coder:14b model...
    ollama pull qwen2.5-coder:14b
)

echo Starting LordCoder with Python 3.12...
echo Model: qwen2.5-coder:14b
echo Configuration: lordcoder.yml
echo.

python3.12 -m aider --config lordcoder.yml

if errorlevel 1 (
    echo.
    echo LordCoder exited with error
    echo.
    echo Troubleshooting:
    echo   1. Make sure Ollama is running: ollama serve
    echo   2. Check model: ollama list
    echo   3. Reinstall aider: install-aider-312.bat
    echo.
)

pause
