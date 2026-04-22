"""
Test Yahoo Finance symbol mapping and fetch correct data
"""
import yfinance as yf
import json

# Test symbols from your data
test_symbols = {
    'ABBV.us': 'ABBV',           # Should be AbbVie Inc.
    'ABN.nl': 'ABN.AS',          # Should be ABN AMRO Bank
    'ADS.de': 'ADS.DE',          # Should be Adidas AG
    '6857.jp': '6857.T',         # Should be Panasonic
    'AEM.ca': 'AEM.TO',          # Should be Agnico Eagle Mines
}

print("Testing Yahoo Finance symbol mapping...\n")

for fxcm_symbol, yahoo_symbol in test_symbols.items():
    print(f"Testing: {fxcm_symbol} -> {yahoo_symbol}")
    try:
        ticker = yf.Ticker(yahoo_symbol)
        info = ticker.info
        
        if info and 'currentPrice' in info:
            print(f"  ✓ Name: {info.get('shortName', 'N/A')}")
            print(f"  ✓ Price: ${info.get('currentPrice', 'N/A')}")
            print(f"  ✓ Currency: {info.get('currency', 'N/A')}")
            print(f"  ✓ Exchange: {info.get('exchange', 'N/A')}")
        else:
            print(f"  ✗ No data available")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    print()

print("\n" + "="*60)
print("Now checking your current stocks-data.json for issues...")
print("="*60 + "\n")

# Load current data
with open('stocks-data.json', 'r') as f:
    stocks = json.load(f)

# Check first 10 stocks
print("First 10 stocks in your data:")
for i, stock in enumerate(stocks[:10], 1):
    print(f"{i:2}. {stock['code']:12} | {stock.get('name', 'NO NAME'):30} | ${stock.get('price', 'N/A'):>10}")
