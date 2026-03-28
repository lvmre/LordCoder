@echo off
echo ========================================
echo   Install Aider with Python 3.12
echo ========================================
echo.

echo Checking Python 3.12 installation...
python3.12 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.12 not found
    echo Please install Python 3.12 first
    echo Download from: https://www.python.org/downloads/release/python-3128/
    pause
    exit /b 1
)

echo [SUCCESS] Python 3.12 found
python3.12 --version
echo.

echo [1/3] Upgrading pip in Python 3.12...
python3.12 -m pip install --upgrade pip
echo.

echo [2/3] Installing aider-chat...
python3.12 -m pip install aider-chat==0.13.0
echo.

echo [3/3] Installing additional dependencies...
python3.12 -m pip install psutil pytest pytest-cov
echo.

echo Testing installation...
python3.12 -m aider --version
if errorlevel 1 (
    echo ERROR: aider installation failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo You can now start LordCoder with:
echo   python3.12 -m aider --config lordcoder.yml
echo.
echo Or create a shortcut/launcher script
pause
