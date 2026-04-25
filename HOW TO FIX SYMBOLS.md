# How to Fix Incorrect Yahoo Finance Symbols

## Quick Guide

You now have a **Symbol Mappings Manager** to fix any incorrect stock symbols!

---

## Method 1: Use the Visual Interface (Easiest) ✨

1. **Open the dashboard**: http://localhost:8001
2. **Click**: "🔗 Fix Symbols" button in the header
3. **Add a mapping**:
   - **FXCM Code**: Enter the stock code (e.g., `ABBV.us`)
   - **Yahoo Symbol**: Enter correct Yahoo symbol (e.g., `ABBV`)
   - Click "Add Mapping"
4. **Download the file**: It will automatically download `custom-symbol-mappings.json`
5. **Replace the file**: Move the downloaded file to replace the old one in your FX Sheet folder
6. **Run update**: Use GitHub Actions or "Update Stock Data.bat" to fetch fresh data

---

## Method 2: Edit the JSON File Directly

1. **Open**: `custom-symbol-mappings.json` in any text editor
2. **Add mappings** in this format:

```json
{
  "_comment": "Custom Yahoo Finance symbol mappings",
  "_instructions": "Format: 'FXCM_SYMBOL': 'YAHOO_SYMBOL'",
  "mappings": {
    "ABBV.us": "ABBV",
    "ABN.nl": "ABN.AS",
    "ADS.de": "ADS.DE",
    "6857.jp": "6857.T",
    "AEM.ca": "AEM.TO",
    "YOUR.STOCK": "CORRECT_SYMBOL"
  }
}
```

3. **Save** the file
4. **Run update**: Fetch fresh data using GitHub Actions or batch file

---

## Finding the Correct Yahoo Finance Symbol

### Method 1: Yahoo Finance Website
1. Go to https://finance.yahoo.com
2. Search for your stock
3. Look at the URL: `https://finance.yahoo.com/quote/ABBV`
4. The symbol is: `ABBV`

### Method 2: Examples by Country

| Country | FXCM Format | Yahoo Format | Example |
|---------|-------------|--------------|---------|
| **USA** | ABBV.us | ABBV | Apple → AAPL |
| **Netherlands** | ABN.nl | ABN.AS | ABN AMRO |
| **Germany** | ADS.de | ADS.DE | Adidas |
| **Japan** | 6857.jp | 6857.T | Panasonic |
| **Canada** | AEM.ca | AEM.TO | Agnico Eagle |
| **Australia** | BHP.au | BHP.AX | BHP Group |
| **UK** | VOD.gb | VOD.L | Vodafone |
| **France** | AI.fr | AI.PA | Air Liquide |

### Common Yahoo Finance Suffixes:
- `.AS` = Amsterdam (Netherlands)
- `.DE` = XETRA (Germany)
- `.T` = Tokyo (Japan)
- `.TO` = Toronto (Canada)
- `.AX` = Australia
- `.L` = London (UK)
- `.PA` = Paris (France)
- `.MI` = Milan (Italy)
- `.MC` = Madrid (Spain)
- `.SW` = Switzerland
- `.ST` = Stockholm (Sweden)

---

## How It Works

1. When fetching data, the system **first checks** `custom-symbol-mappings.json`
2. If a custom mapping exists, it uses that symbol
3. If not, it uses the automatic conversion
4. This ensures your corrections are always applied

---

## Example: Fixing a Wrong Stock

**Problem**: Stock "XYZ.de" is showing wrong price

**Solution**:
1. Go to Yahoo Finance and search for the correct company
2. Find the URL: `https://finance.yahoo.com/quote/XYZ.DE`
3. Add mapping: `"XYZ.de": "XYZ.DE"`
4. Run update
5. ✅ Now it fetches correct data!

---

## Testing Your Mappings

After adding mappings:

1. **Run update** (GitHub Actions or batch file)
2. **Check the log** to see if custom mappings were used
3. **Verify** the stock now shows correct name and price
4. **Refresh** your dashboard

---

## Tips

- ✅ Always test a few stocks first before updating all 463
- ✅ Use the visual manager for easy editing
- ✅ Keep the JSON file format valid (use quotes, commas)
- ✅ The system logs which custom mappings are used
- ✅ You can delete mappings if they're no longer needed

---

## Need Help?

If you're unsure about a symbol:
1. Search for the stock on Yahoo Finance
2. Check the URL for the correct symbol
3. Add it to the mappings
4. Test with a small update first

---

**Your custom mappings file**: `custom-symbol-mappings.json`
**Manager page**: http://localhost:8001/symbol-mappings-manager.html
