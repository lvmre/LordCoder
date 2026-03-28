@echo off
echo ========================================
echo        Starting LordCoder AI
echo ========================================
echo.

:: Check if PATH is set up for uv tools
aider --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Setting up PATH for uv tools...
    $env:PATH = "C:\Users\lovem\.local\bin;$env:PATH" 2>nul
    set PATH=%USERPROFILE%\.local\bin;%PATH%
)

:: Check if aider is available
aider --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: aider not found. Please run install.bat first.
    echo.
    echo To install:
    echo   install.bat
    echo.
    pause
    exit /b 1
)

:: Check if configuration exists
if not exist "lordcoder.yml" (
    echo ERROR: lordcoder.yml not found in current directory
    echo Make sure you're in the LordCoder project folder
    pause
    exit /b 1
)

echo [SUCCESS] Starting LordCoder with configuration...
echo.
echo Model: qwen2.5-coder:14b (balanced for your system)
echo Configuration: lordcoder.yml
echo.
echo Press Ctrl+C to exit LordCoder
echo.

:: Start LordCoder
aider --config lordcoder.yml

if errorlevel 1 (
    echo.
    echo LordCoder exited with an error.
    echo.
    echo Troubleshooting:
    echo   1. Make sure Ollama is running: ollama serve
    echo   2. Check the model is installed: ollama list
    echo   3. See TROUBLESHOOTING.md for more help
    echo.
)

pause
