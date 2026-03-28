@echo off
echo ========================================
echo        LordCoder Simple Launcher
echo ========================================
echo.

:: Check if Ollama is working
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama not found. Please install from https://ollama.com
    pause
    exit /b 1
)

:: Check model is available
ollama list | findstr "qwen2.5-coder" >nul 2>&1
if errorlevel 1 (
    echo Downloading qwen2.5-coder:14b model...
    ollama pull qwen2.5-coder:14b
)

echo Starting LordCoder...
echo Model: qwen2.5-coder:14b
echo Configuration: lordcoder.yml
echo.
echo NOTE: If this doesn't work, you need to install aider-chat manually:
echo   pip install aider-chat==0.13.0
echo   Then run: aider --config lordcoder.yml
echo.

:: Try the most basic approach
aider --config lordcoder.yml

if errorlevel 1 (
    echo.
    echo LordCoder could not start automatically.
    echo.
    echo Manual setup instructions:
    echo   1. Install: pip install aider-chat==0.13.0
    echo   2. Run: aider --config lordcoder.yml
    echo.
    echo Or run: install.bat for complete setup
)

pause
