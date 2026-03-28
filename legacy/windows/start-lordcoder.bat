@echo off
setlocal EnableDelayedExpansion
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

set "MODEL="
set "PROVIDER="
set "EFFECTIVE_CONFIG="
set "OLLAMA_MODEL="
for /f "tokens=1,* delims==" %%A in ('python -m src.lordcoder.model_selector') do (
    if /I "%%A"=="MODEL" set "MODEL=%%B"
    if /I "%%A"=="PROVIDER" set "PROVIDER=%%B"
    if /I "%%A"=="EFFECTIVE_CONFIG" set "EFFECTIVE_CONFIG=%%B"
    if /I "%%A"=="OLLAMA_MODEL" set "OLLAMA_MODEL=%%B"
)
if errorlevel 1 (
    echo ERROR: Failed to prepare model selection.
    pause
    exit /b 1
)
if "%MODEL%"=="" (
    echo ERROR: No model was selected.
    pause
    exit /b 1
)

if /I "%PROVIDER%"=="ollama" (
    ollama --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Ollama is required for model %MODEL%
        echo Install Ollama from https://ollama.com
        pause
        exit /b 1
    )

    ollama show "%OLLAMA_MODEL%" >nul 2>&1
    if errorlevel 1 (
        set /p PULL_MODEL=The Ollama model "%OLLAMA_MODEL%" is not installed. Pull it now? [Y/N]: 
        if /I not "!PULL_MODEL!"=="Y" (
            if /I not "!PULL_MODEL!"=="y" (
                echo Run this command when you're ready: ollama pull %OLLAMA_MODEL%
                pause
                exit /b 1
            )
        )

        echo Downloading %OLLAMA_MODEL%...
        ollama pull "%OLLAMA_MODEL%"
        if errorlevel 1 (
            echo ERROR: Failed to download %OLLAMA_MODEL%
            pause
            exit /b 1
        )
    )
)

echo [SUCCESS] Starting LordCoder with configuration...
echo.
echo Model: %MODEL%
echo Configuration: %EFFECTIVE_CONFIG%
echo.
echo Press Ctrl+C to exit LordCoder
echo.

:: Start LordCoder
aider --config "%EFFECTIVE_CONFIG%"

if errorlevel 1 (
    echo.
    echo LordCoder exited with an error.
    echo.
    echo Troubleshooting:
    echo   1. Re-run this launcher and confirm the selected model
    echo   2. If using Ollama, make sure Ollama is running: ollama serve
    echo   3. See TROUBLESHOOTING.md for more help
    echo.
)

pause
