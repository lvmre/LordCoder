@echo off
echo ========================================
echo        Starting LordCoder AI
echo ========================================
echo.

:: Check if Ollama is running
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama not found. Please install from https://ollama.com
    pause
    exit /b 1
)

:: Check if the AI model is available
ollama list | findstr "qwen2.5-coder" >nul 2>&1
if errorlevel 1 (
    echo WARNING: qwen2.5-coder model not found
    echo Downloading qwen2.5-coder:14b...
    ollama pull qwen2.5-coder:14b
    if errorlevel 1 (
        echo ERROR: Failed to download model
        pause
        exit /b 1
    )
)

:: Try different methods to start aider
echo Starting LordCoder...
echo.

:: Method 1: Direct aider command
aider --config lordcoder.yml --no-repo-map
if not errorlevel 1 goto :success

:: Method 2: Use python -m uv tool run
echo.
echo Trying alternative method...
python -m uv tool run aider --config lordcoder.yml --no-repo-map
if not errorlevel 1 goto :success

:: Method 3: Use virtual environment
echo.
echo Trying virtual environment method...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    aider --config lordcoder.yml --no-repo-map
    if not errorlevel 1 goto :success
)

echo.
echo ERROR: All methods failed to start LordCoder
echo.
echo Troubleshooting:
echo   1. Make sure Ollama is running: ollama serve
echo   2. Check the model: ollama list
echo   3. Try reinstalling: install.bat
echo   4. See TROUBLESHOOTING.md for more help
echo.
pause
exit /b 1

:success
echo.
echo LordCoder started successfully!
echo Press Ctrl+C to exit
pause
