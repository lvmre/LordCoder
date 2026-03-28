@echo off
setlocal EnableDelayedExpansion
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

set "MODEL="
set "PROVIDER="
set "EFFECTIVE_CONFIG="
set "OLLAMA_MODEL="
for /f "tokens=1,* delims==" %%A in ('python3.12 -m src.lordcoder.model_selector') do (
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
        echo Install from: https://ollama.com
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

echo Starting LordCoder with Python 3.12...
echo Model: %MODEL%
echo Configuration: %EFFECTIVE_CONFIG%
echo.

python3.12 -m aider --config "%EFFECTIVE_CONFIG%"

if errorlevel 1 (
    echo.
    echo LordCoder exited with error
    echo.
    echo Troubleshooting:
    echo   1. Re-run this launcher and confirm the selected model
    echo   2. If using Ollama, make sure Ollama is running: ollama serve
    echo   3. Reinstall aider: install-aider-312.bat
    echo.
)

pause
