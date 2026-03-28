@echo off
setlocal EnableDelayedExpansion
echo ========================================
echo        Starting LordCoder AI
echo ========================================
echo.

:: Prepare the effective configuration and selected model
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

:: Try different methods to start aider
echo Starting LordCoder...
echo Selected model: %MODEL%
echo Configuration: %EFFECTIVE_CONFIG%
echo.

:: Method 1: Direct aider command
aider --config "%EFFECTIVE_CONFIG%" --no-repo-map
if not errorlevel 1 goto :success

:: Method 2: Use python -m uv tool run
echo.
echo Trying alternative method...
python -m uv tool run aider --config "%EFFECTIVE_CONFIG%" --no-repo-map
if not errorlevel 1 goto :success

:: Method 3: Use virtual environment
echo.
echo Trying virtual environment method...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    aider --config "%EFFECTIVE_CONFIG%" --no-repo-map
    if not errorlevel 1 goto :success
)

echo.
echo ERROR: All methods failed to start LordCoder
echo.
echo Troubleshooting:
echo   1. Re-run this launcher and confirm the selected model
echo   2. If using Ollama, make sure Ollama is running: ollama serve
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
