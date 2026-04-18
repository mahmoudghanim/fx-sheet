@echo off
title FX Sheet - Update Stock Data
cls

echo ================================================================
echo              FX Sheet - Stock Data Updater
echo ================================================================
echo.
echo This will update all 463 stocks with fresh data from Yahoo Finance
echo and push the changes to GitHub automatically.
echo.
echo Time required: 1-2 minutes
echo.
pause

echo.
echo ================================================================
echo Step 1: Fetching fresh stock data...
echo ================================================================
echo.

python update_stocks.py

if errorlevel 1 (
    echo.
    echo ================================================================
    echo ERROR: Failed to update stock data!
    echo ================================================================
    echo.
    echo Please check:
    echo 1. Python is installed
    echo 2. yfinance package is installed (pip install yfinance pandas)
    echo 3. You have an internet connection
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo Step 2: Saving changes to GitHub...
echo ================================================================
echo.

git add stocks-data.json
git commit -m "Update stock data - %date% %time%"

if errorlevel 1 (
    echo.
    echo No changes to commit (data is already up to date)
    echo.
    pause
    exit /b 0
)

git push

if errorlevel 1 (
    echo.
    echo ================================================================
    echo ERROR: Failed to push to GitHub!
    echo ================================================================
    echo.
    echo Please check:
    echo 1. You are connected to the internet
    echo 2. Git is configured with your GitHub credentials
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo                    UPDATE COMPLETE!
echo ================================================================
echo.
echo Your stock data has been updated and pushed to GitHub.
echo.
echo Next steps:
echo 1. Refresh your GitHub Pages dashboard to see new data
echo 2. Or visit: https://github.com/mahmoudghanim/fx-sheet/actions
echo    to view the workflow status
echo.
echo ================================================================
pause
