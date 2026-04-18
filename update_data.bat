@echo off
echo ============================================================
echo Global Stocks Dashboard - Data Updater
echo ============================================================
echo.
echo Fetching real-time stock data from Yahoo Finance...
echo.

python update_stocks.py

echo.
echo ============================================================
echo Update Complete!
echo ============================================================
echo.
echo To view your dashboard:
echo   1. Run: python server.py
echo   2. Open: http://localhost:8000
echo.
pause
