@echo off
title FX Sheet Dashboard
cls
echo ========================================
echo   FX Sheet Stock Dashboard
echo ========================================
echo.
echo Starting dashboard server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Start the server
python server.py

REM If server stops, keep window open
echo.
echo Server stopped.
echo Press any key to exit...
pause >nul
