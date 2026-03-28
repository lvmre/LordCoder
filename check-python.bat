@echo off
echo ========================================
echo     Python Installation Check
echo ========================================
echo.

echo Current Python versions:
echo.

echo Python 3.13 (current):
python --version 2>nul || echo Python 3.13 not found
echo.

echo Python 3.12 (new):
python3.12 --version 2>nul || echo Python 3.12 not found
echo.

echo Python launcher (py):
py -3.12 --version 2>nul || echo py launcher for 3.12 not found
echo.

echo Available Python installations:
py -0p
echo.

pause
