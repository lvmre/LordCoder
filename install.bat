@echo off
echo ========================================
echo    LordCoder AI Environment Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Detected Python version: %PYTHON_VERSION%

:: Check if uv is installed
python -m uv --version >nul 2>&1
if errorlevel 1 (
    echo [1/6] Installing uv package manager...
    python -m pip install uv
    if errorlevel 1 (
        echo ERROR: Failed to install uv
        pause
        exit /b 1
    )
) else (
    echo [1/6] uv already installed
)

:: Setup PATH for uv tools
echo [2/6] Setting up environment...
$env:PATH = "C:\Users\lovem\.local\bin;$env:PATH" 2>nul
set PATH=%USERPROFILE%\.local\bin;%PATH%

:: Install aider-chat using uv (recommended method)
echo [3/6] Installing aider-chat with uv...
python -m uv tool install --force --python python3.12 aider-chat
if errorlevel 1 (
    echo WARNING: uv installation failed, trying fallback method...
    goto :fallback_install
)

:: Check if aider is available
aider --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: aider installation failed
    goto :fallback_install
) else (
    echo [SUCCESS] aider-chat installed successfully
    goto :check_ollama
)

:fallback_install
echo [FALLBACK] Using traditional pip installation...
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install aider-chat==0.13.0 psutil pytest pytest-cov
if errorlevel 1 (
    echo ERROR: Fallback installation also failed
    pause
    exit /b 1
)

:check_ollama
echo [4/6] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama is not installed or not in PATH
    echo Please download and install Ollama from https://ollama.com
    echo After installation, run: ollama pull qwen2.5-coder:14b
    echo.
) else (
    echo [SUCCESS] Ollama found
    goto :check_model
)

:check_model
echo [5/6] Checking AI model...
ollama list | findstr "qwen2.5-coder" >nul 2>&1
if errorlevel 1 (
    echo [INFO] No qwen2.5-coder model found
    echo [5/6] Downloading AI model (this may take a while)...
    ollama pull qwen2.5-coder:14b
    if errorlevel 1 (
        echo WARNING: Failed to pull qwen2.5-coder:14b model
        echo You can pull it later with: ollama pull qwen2.5-coder:14b
        echo For more power, try: ollama pull qwen2.5-coder:32b
        echo For less RAM, try: ollama pull qwen2.5-coder:7b
    ) else (
        echo [SUCCESS] qwen2.5-coder:14b model downloaded
    )
) else (
    echo [SUCCESS] qwen2.5-coder model already available
)

echo [6/6] Testing LordCoder configuration...
if exist "lordcoder.yml" (
    echo [SUCCESS] Configuration file found
) else (
    echo WARNING: lordcoder.yml not found
)

echo.
echo ========================================
echo         Setup Complete!
echo ========================================
echo.
echo System Information:
echo   Python: %PYTHON_VERSION%
echo   Installation: uv-based (recommended)
echo   Model: qwen2.5-coder:14b (balanced for your system)
echo.
echo To start LordCoder:
echo   METHOD 1 (uv-based):   aider --config lordcoder.yml
echo   METHOD 2 (fallback):   .venv\Scripts\activate && aider --config lordcoder.yml
echo.
echo Performance Tips:
echo   - qwen2.5-coder:14b provides good speed on your i5-10400
echo   - Upgrade to :32b for more complex tasks if needed
echo   - Use :7b if you experience performance issues
echo.
echo Troubleshooting:
echo   - If 'aider' is not found, restart your terminal
echo   - Check Ollama is running: ollama serve
echo   - See README.md for detailed troubleshooting
echo.
pause
