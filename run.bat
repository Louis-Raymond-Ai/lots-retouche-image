@echo off
REM Logo Processor - Windows Launcher
REM Double-click this file to run the application

echo.
echo ========================================
echo   Logo Processor - Starting...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    echo.
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install requirements
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

REM Run the main script
python main.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo An error occurred. Please check the messages above.
    pause
)

exit /b 0
