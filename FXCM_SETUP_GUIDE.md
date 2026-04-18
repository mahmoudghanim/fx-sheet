# FXCM Stock Data Integration Guide

## Overview
This guide explains how to fetch real-time stock data from FXCM for your Global Stocks Dashboard.

---

## 📋 Current Status

✅ **Dashboard Features:**
- Frozen header table with 463 global stocks
- Sorting by any column (click headers)
- Advanced filtering (search, country, price range, volume, 52W change)
- Auto-refresh every 5 minutes

⚠️ **Data Status:**
- Currently using sample data for demonstration
- Need to connect to FXCM for real-time data

---

## 🔑 Option 1: FXCM Forex Connect API (Official Method)

### Prerequisites
- **Python Version:** Must use Python 3.5, 3.6, or 3.7
- **FXCM Account:** Demo or Real account with Trading Station credentials
- **Forex Connect API:** Free to download and use

### Step-by-Step Setup

#### Step 1: Install Python 3.7

**Option A - Using Conda (Recommended):**
```bash
conda create -n fxcm python=3.7
conda activate fxcm
```

**Option B - Download from Python.org:**
- Download: https://www.python.org/downloads/release/python-379/
- Install and add to PATH

#### Step 2: Install Forex Connect API

```bash
pip install forexconnect
```

**Alternative:** Download from:
- Main page: https://github.com/fxcm/ForexConnectAPI
- Downloads: http://fxcodebase.com/wiki/index.php/Download

#### Step 3: Get Your FXCM Credentials

Your credentials are the **same as your Trading Station login**:
- **Username:** Your FXCM account username
- **Password:** Your FXCM account password
- **Account Type:** "Demo" or "Real"
- **Connection URL:** www.fxcorporate.com/Hosts.jsp

**Don't have an account?**
1. Go to https://www.fxcm.com/
2. Create a FREE demo account
3. Download Trading Station to verify credentials

#### Step 4: Configure the Script

Open `fetch_fxcm_data.py` and update:

```python
FXCM_USERNAME = "your_actual_username"
FXCM_PASSWORD = "your_actual_password"
FXCM_ACCOUNT_TYPE = "Demo"  # or "Real"
FXCM_URL = "www.fxcorporate.com/Hosts.jsp"
```

#### Step 5: Run the Script

```bash
python fetch_fxcm_data.py
```

The script will:
- Connect to FXCM
- Fetch real-time prices, volume, and market data
- Update `stocks-data.json`
- Your dashboard will automatically display the new data

---

## 📊 Option 2: Yahoo Finance API (Easiest Alternative)

### Why Yahoo Finance?
- ✅ **Free** - no authentication required
- ✅ **Works with any Python version**
- ✅ **Easy to set up** - works in 5 minutes
- ✅ **Reliable** - widely used by developers
- ✅ **Global coverage** - US, European, Asian stocks

### Setup

#### Step 1: Install yfinance

```bash
pip install yfinance
```

#### Step 2: I'll Create the Integration Script

Let me know if you want this option, and I'll create a complete script that:
- Maps your FXCM stock symbols to Yahoo Finance symbols
- Fetches real-time prices, volume, 52-week ranges
- Updates your JSON data file
- Can run on a schedule for automatic updates

---

## 📤 Option 3: Export from Trading Station

If you have Trading Station installed:

1. Open Trading Station
2. Navigate to your watchlist with the stocks
3. Export the data (File → Export or right-click → Export)
4. Save as CSV/Excel file
5. I'll create a script to import and convert it

---

## 📚 FXCM API Resources

- **API Comparison:** https://www.fxcm.com/au/algorithmic-trading/compare-api/
- **Forex Connect Docs:** http://fxcodebase.com/wiki/index.php/Category:ForexConnect
- **Python Examples:** https://github.com/gehtsoft/forex-connect/tree/master/samples/Python
- **Python Package:** https://pypi.org/project/forexconnect/
- **Single Shares CFD List:** https://docs.fxcorporate.com/user-guide/FXCMSSCFDProductList.pdf

### Online Help
- C++/C#/Java/Python: https://fxcodebase.com/bin/forexconnect/1.6.5/help/

---

## 🔄 Data Update Options

### Manual Update
```bash
python fetch_fxcm_data.py
```
Then refresh your browser.

### Automatic Update (Scheduled)
I can create a scheduler that:
- Runs every X minutes/hours
- Fetches latest data from FXCM
- Updates your JSON file
- Dashboard auto-refreshes

### Real-time Update
- Web page already refreshes every 5 minutes
- Just need to set up data source

---

## 🎯 Recommended Next Steps

**For Quick Testing (Now):**
- ✅ Sample data is already generated
- Refresh your browser to see it

**For Real Data (Choose One):**

1. **Fastest Setup (10 mins):** Yahoo Finance API
   - Any Python version
   - No credentials needed
   - I can set this up right now

2. **Official FXCM Data (30 mins):** Forex Connect API
   - Requires Python 3.7
   - Needs FXCM account
   - Most accurate for FXCM symbols

3. **Manual Export:** Trading Station
   - Export data yourself
   - I'll create import script

---

## ❓ Which Option Do You Prefer?

Let me know and I'll:
1. Set up the integration
2. Create the necessary scripts
3. Test it with your stock list
4. Configure automatic updates

**My recommendation:** Start with Yahoo Finance for immediate results, then optionally add FXCM Forex Connect API later if you need FXCM-specific data.

---

## 📁 Project Files

- `index.html` - Main dashboard web page
- `stocks-data.json` - Stock data (auto-updated)
- `convert_to_json.py` - Excel to JSON converter
- `fetch_fxcm_data.py` - FXCM Forex Connect API integration
- `scrape_fxcm.py` - Alternative data fetching options
- `server.py` - Local web server
- `Listing.xlsx` - Your original stock list

---

## 💡 Tips

1. **Keep the server running** in background for dashboard access
2. **Bookmark** http://localhost:8000 for quick access
3. **Data refreshes** automatically every 5 minutes
4. **Sort and filter** to find stocks quickly
5. **Add more columns** anytime - just let me know!
