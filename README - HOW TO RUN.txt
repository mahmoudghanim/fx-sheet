================================================================
          FX SHEET DASHBOARD - QUICK START GUIDE
================================================================

TO START THE DASHBOARD:
-----------------------
1. Double-click:  Start Dashboard.bat
   OR
2. Right-click:   Start Dashboard.ps1 → Run with PowerShell

The dashboard will open automatically in your browser!

URL: http://localhost:8001


TO UPDATE STOCK DATA:
---------------------
Double-click:  update_data.bat
Wait 5-10 minutes for the update to complete.


IMPORTANT:
----------
- Keep the dashboard window OPEN while using the website
- Close the window when you're done to stop the server
- Press Ctrl+C to stop the server manually


TROUBLESHOOTING:
----------------
Problem: "Python is not installed"
Solution: Install Python from https://www.python.org/downloads/
          Make sure to check "Add Python to PATH" during install

Problem: "Port is already in use"
Solution: Close any other dashboard windows that are running

Problem: Dashboard not showing data
Solution: Run update_data.bat and refresh browser (Ctrl+Shift+R)


FEATURES:
---------
✓ 463 Global Stocks with real-time data
✓ Filter by Country, Industry, Currency
✓ Filter by Price, Volume, 52-Week Change
✓ Click stock names to view on Yahoo Finance
✓ Sort by any column
✓ Fast pagination (50 stocks per page)


FILES:
------
Start Dashboard.bat     ← Main launcher (recommended)
Start Dashboard.ps1     ← PowerShell launcher (alternative)
update_data.bat         ← Update stock prices
server.py               ← Web server
index.html              ← Dashboard interface
stocks-data.json        ← Stock data


ENJOY TRACKING YOUR STOCKS! 📈
================================================================
