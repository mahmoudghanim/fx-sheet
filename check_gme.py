import yfinance as yf
import json

# Check GME data
gme = yf.Ticker('GME')
info = gme.info

print("GME (GameStop) Data from Yahoo Finance:")
print("=" * 60)
print(f"Current Price: ${info.get('currentPrice', 'N/A')}")
print(f"Regular Market Price: ${info.get('regularMarketPrice', 'N/A')}")
print(f"Previous Close: ${info.get('previousClose', 'N/A')}")
print(f"Day High: ${info.get('dayHigh', 'N/A')}")
print(f"Day Low: ${info.get('dayLow', 'N/A')}")
print(f"Volume: {info.get('regularMarketVolume', 'N/A')}")
print(f"52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
print(f"52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")
print(f"Market Cap: ${info.get('marketCap', 'N/A')}")
print()

# Check what we stored
with open('stocks-data.json', 'r') as f:
    data = json.load(f)
    gme_stored = [s for s in data if s['code'] == 'GME.us'][0]
    
print("GME Data in stocks-data.json:")
print("=" * 60)
print(f"Price: ${gme_stored['price']}")
print(f"Volume: {gme_stored['volume']}")
print(f"52 Week High: ${gme_stored['week52High']}")
print(f"52 Week Low: ${gme_stored['week52Low']}")
print(f"Change Amount: ${gme_stored['changeAmount']}")
print(f"Change %: {gme_stored['change52W']}%")
print()

# Verify with historical data
print("Recent Historical Data (Last 5 Days):")
print("=" * 60)
hist = gme.history(period="5d")
print(hist[['Close', 'Volume']].to_string())
