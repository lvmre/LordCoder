@echo off
setlocal EnableDelayedExpansion
echo ========================================
echo        LordCoder Simple Launcher
echo ========================================
echo.

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
        if /I "!PULL_MODEL!"=="Y" (
            ollama pull "%OLLAMA_MODEL%"
        ) else if /I "!PULL_MODEL!"=="y" (
            ollama pull "%OLLAMA_MODEL%"
        ) else (
            echo Run this command when you're ready: ollama pull %OLLAMA_MODEL%
            pause
            exit /b 1
        )

        if errorlevel 1 (
            echo ERROR: Failed to download %OLLAMA_MODEL%
            pause
            exit /b 1
        )
    )
)

echo Starting LordCoder...
echo Model: %MODEL%
echo Configuration: %EFFECTIVE_CONFIG%
echo.
echo NOTE: If this doesn't work, you need to install aider-chat manually:
echo   pip install aider-chat==0.13.0
echo   Then run: aider --config %EFFECTIVE_CONFIG%
echo.

:: Try the most basic approach
aider --config "%EFFECTIVE_CONFIG%"

if errorlevel 1 (
    echo.
    echo LordCoder could not start automatically.
    echo.
    echo Manual setup instructions:
    echo   1. Install: pip install aider-chat==0.13.0
    echo   2. Run: aider --config %EFFECTIVE_CONFIG%
    echo.
    echo Or run: install.bat for complete setup
)

pause
