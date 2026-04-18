"""
FXCM API Credentials Configuration
===================================
IMPORTANT: Keep this file secure and do not share it!

Instructions:
1. Replace the placeholder values below with your actual FXCM credentials
2. Your credentials are the same as your Trading Station login
3. Save this file

To get FXCM credentials:
- Go to https://www.fxcm.com/
- Create a demo account (free) or use your real account
- Use the same username/password as Trading Station
"""

# FXCM Account Credentials
FXCM_USERNAME = "D251099224"      # Your FXCM username (Trading Station login)
FXCM_PASSWORD = "w5cpM"      # Your FXCM password (Trading Station password)
FXCM_ACCOUNT_TYPE = "Demo"                # Use "Demo" for demo account, "Real" for live account

# Connection URL (do not change)
FXCM_URL = "www.fxcorporate.com/Hosts.jsp"

# Data Settings
UPDATE_INTERVAL_MINUTES = 5              # How often to update data (in minutes)
SAVE_TO_FILE = "stocks-data.json"        # Output file for stock data
LOG_FILE = "fxcm_fetch.log"              # Log file for debugging

# Optional: Specific stocks to prioritize (leave empty for all stocks)
PRIORITY_STOCKS = [
    # Add stock symbols here if you want to fetch certain stocks first
    # Example: "AAPL", "MSFT", "GOOGL"
]
