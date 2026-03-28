@echo off
echo Setting up environment...

:: Set PATH for both uv tools and Ollama
set PATH=%USERPROFILE%\.local\bin;C:\Users\lovem\AppData\Local\Programs\Ollama;%PATH%

echo Starting LordCoder...
echo.

:: Try to run aider
aider --config lordcoder.yml --no-repo-map

if errorlevel 1 (
    echo.
    echo LordCoder failed to start. Trying alternative method...
    echo.
    
    :: Fallback: use python -m uv tool run
    python -m uv tool run aider --config lordcoder.yml --no-repo-map
)

pause
