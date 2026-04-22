# Stock Data Issue - Explanation & Fix

## The Problem

Your stock data has **incorrect company names** because:
1. The original data came from FXCM which had limited name information
2. Example: "ABBV.us" shows name as "Inc." instead of "AbbVie Inc."
3. Prices might also be incorrect if the wrong Yahoo Finance symbol was used

## The Fix Applied

I've updated `fetch_yahoo_data.py` to:
1. ✅ Fetch **correct company names** from Yahoo Finance (`shortName` and `longName` fields)
2. ✅ Update stock names when fetching fresh data
3. ✅ Properly map FXCM symbols to Yahoo Finance symbols

## How to Get Correct Data

### **Option 1: Use GitHub Actions (Recommended)** ✨

The GitHub Actions workflow uses Python 3.10 which has full yfinance support:

1. Go to: https://github.com/mahmoudghanim/fx-sheet/actions
2. Click **"Update FX Sheet Stock Data"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 2-3 minutes
5. **Result**: All 463 stocks will have:
   - ✅ Correct company names
   - ✅ Accurate prices
   - ✅ Proper daily change percentages

### **Option 2: Use Python 3.10+ Locally**

If you want to update locally, you need Python 3.8 or higher:

```bash
# Check Python version
python --version

# If Python 3.7, install newer Python from python.org
# Then run:
py -3.10 update_stocks.py
```

### **Option 3: Manual Fix (Quick)**

If you just need a few stocks fixed right now:

1. Open `stocks-data.json` in a text editor
2. Find the stock with wrong name
3. Update the `name` field manually
4. Save and refresh dashboard

## Symbol Mapping Reference

The system converts FXCM symbols to Yahoo Finance symbols:

| FXCM Format | Yahoo Finance | Example |
|-------------|---------------|---------|
| AAPL.us | AAPL | Apple Inc. |
| ABN.nl | ABN.AS | ABN AMRO Bank (Amsterdam) |
| ADS.de | ADS.DE | Adidas AG (Germany) |
| 6857.jp | 6857.T | Panasonic (Tokyo) |
| AEM.ca | AEM.TO | Agnico Eagle Mines (Toronto) |
| BHP.au | BHP.AX | BHP Group (Australia) |

## What Was Fixed in the Code

**Before:**
```python
# Only fetched price data, kept old names
stock['price'] = data['currentPrice']
# Name stayed as "Inc." or incorrect
```

**After:**
```python
# Fetch price AND update company name
stock['price'] = data['currentPrice']
stock['name'] = data.get('shortName') or data.get('longName')
# Now shows "AbbVie Inc." correctly
```

## Expected Results After Update

**Before (Wrong):**
```
ABBV.us | Inc.                    | $202.93
ABN.nl  | Amro Bank NV            | $29.88
6857.jp | [Japanese characters]   | ¥1,234
```

**After (Correct):**
```
ABBV.us | AbbVie Inc.             | $205.50
ABN.nl  | ABN AMRO Bank N.V.      | €30.15
6857.jp | Panasonic Holdings Corp | ¥1,250
```

## Next Steps

1. **Run the GitHub Actions workflow** (easiest method)
2. Wait for it to complete (~2-3 minutes)
3. Refresh your dashboard
4. All stocks will have correct names and prices! ✨

---

**Need help?** The workflow will automatically:
- Fetch data for all 463 stocks from Yahoo Finance
- Update company names
- Update prices
- Calculate daily change percentages
- Commit everything to your repository
