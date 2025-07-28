@echo off
echo 🚀 Starting PDP Tracker...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if GUI file exists
if not exist "pdp_gui.py" (
    echo ❌ pdp_gui.py not found in current directory
    echo Please make sure you're running this from the PDP Tracker folder
    pause
    exit /b 1
)

REM Run the PDP Tracker GUI
echo ✅ Launching PDP Tracker GUI...
python pdp_gui.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ An error occurred. Please check the error messages above.
    pause
) 