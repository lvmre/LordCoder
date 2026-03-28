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
    echo You only need Ollama if you plan to use an ollama/... model
    echo.
) else (
    echo [SUCCESS] Ollama found
    goto :check_model
)

:check_model
echo [5/6] Preparing model selection...
echo [INFO] LordCoder now asks you to choose a model on first launch.
echo [INFO] Your selection is saved in .lordcoder-model.
echo [INFO] If you choose an ollama/... model, LordCoder will offer to pull it on demand.

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
echo   Model selection: chosen on first launch and saved locally
echo.
echo To start LordCoder:
echo   METHOD 1 (recommended): start-lordcoder.bat
echo   METHOD 2 (simple):      run-lordcoder.bat
echo   METHOD 3 (fallback):    .venv\Scripts\activate ^&^& aider --config lordcoder.effective.yml
echo.
echo Performance Tips:
echo   - qwen2.5-coder:14b is still a strong balanced preset for your i5-10400
echo   - Choose :32b for more complex tasks if your RAM allows
echo   - Choose :7b if you experience performance issues
echo.
echo Troubleshooting:
echo   - If 'aider' is not found, restart your terminal
echo   - If using Ollama, make sure Ollama is running: ollama serve
echo   - See README.md for detailed troubleshooting
echo.
pause
