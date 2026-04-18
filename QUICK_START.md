# Global Stocks Dashboard - Quick Start Guide

## 🎯 Current Status
- ✅ Dashboard built and working
- ✅ **Real-time data from Yahoo Finance** (463 stocks)
- ✅ FXCM preserved as alternative for future use
- ✅ All stocks updated with live market data

---

## 📋 Quick Start (3 Easy Steps)

### Step 1: Update Stock Data 📊

**Double-click:** `update_data.bat`

**Or run manually:**
```bash
python update_stocks.py
```

This will:
- ✅ Fetch real-time data from Yahoo Finance
- ✅ Update all 463 stocks
- ✅ Show progress in real-time
- ✅ Takes 5-10 minutes

---

### Step 2: Start Dashboard 🌐

**Double-click:** `start_dashboard.bat`

**Or run manually:**
```bash
python server.py
```

Your browser will open automatically to: http://localhost:8000

---

## 🔄 Daily Usage

### Update Data (Anytime):
```bash
python update_stocks.py
```
**Or double-click:** `update_data.bat`

### Start Dashboard:
```bash
python server.py
```
**Or double-click:** `start_dashboard.bat`

### Check Data Status:
```bash
python update_stocks.py --status
```

---

## ⚠️ Troubleshooting

### Error: "No module named 'yfinance'"
```bash
python -m pip install yfinance pandas
```

### Error: "Connection failed"
- Check internet connection
- Some stocks may not be available on Yahoo Finance
- Normal to have 2-5% failure rate for exotic symbols

### Dashboard not updating?
1. Run `python update_stocks.py` to fetch fresh data
2. Refresh browser (F5)
3. Data auto-refreshes every 5 minutes

---

## 📚 File Reference

| File | Purpose |
|------|---------|
| `update_stocks.py` | **Main data fetcher** (Yahoo Finance default) |
| `fetch_yahoo_data.py` | Yahoo Finance integration |
| `update_data.bat` | **Quick update** (double-click) |
| `start_dashboard.bat` | **Start server** (double-click) |
| `stocks-data.json` | Stock data (auto-updated with real data) |
| `index.html` | Your dashboard |
| `server.py` | Web server |

### Alternative (FXCM - Preserved for Future)

| File | Purpose |
|------|---------|
| `fxcm_config.py` | FXCM credentials (if re-enabling FXCM) |
| `fetch_fxcm_data.py` | FXCM data fetcher (alternative) |
| `diagnose_fxcm.py` | FXCM connection diagnostic |
| `setup_fxcm.bat` | FXCM Python 3.7 setup |

---

## 🆘 Need Help?

**Yahoo Finance Resources:**
- Documentation: https://github.com/ranaroussi/yfinance
- Package: https://pypi.org/project/yfinance/

**FXCM Resources (Alternative):**
- Documentation: http://fxcodebase.com/wiki/index.php/Category:ForexConnect
- Python Examples: https://github.com/gehtsoft/forex-connect/tree/master/samples/Python

**Common Issues:**
- Use `python update_stocks.py` for Yahoo Finance (any Python version)
- Use `py -3.7 update_stocks.py --fxcm` for FXCM (Python 3.7 only)
- Dashboard auto-refreshes every 5 minutes

---

## ✅ Checklist

- [x] Yahoo Finance installed and working
- [x] All 463 stocks fetching real data
- [x] Dashboard showing live market data
- [x] Easy batch files for quick updates
- [x] FXCM preserved as alternative

---

**Good luck! 🚀**
