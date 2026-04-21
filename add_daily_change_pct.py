"""
Quick script to add dailyChangePct field to existing stocks-data.json
Calculates daily change percentage from changeAmount and price
"""
import json

print("Adding dailyChangePct field to stocks-data.json...")

# Load existing data
with open('stocks-data.json', 'r') as f:
    stocks = json.load(f)

print(f"Loaded {len(stocks)} stocks")

# Add dailyChangePct field
updated_count = 0
for stock in stocks:
    # Calculate daily change percentage: (changeAmount / (price - changeAmount)) * 100
    if stock.get('price') and stock.get('changeAmount'):
        previous_price = stock['price'] - stock['changeAmount']
        if previous_price != 0:
            daily_change_pct = round((stock['changeAmount'] / previous_price) * 100, 2)
            stock['dailyChangePct'] = daily_change_pct
            updated_count += 1
        else:
            stock['dailyChangePct'] = None
    else:
        stock['dailyChangePct'] = None

# Save updated data
with open('stocks-data.json', 'w') as f:
    json.dump(stocks, f, indent=2)

print(f"✓ Updated {updated_count} stocks with dailyChangePct")
print("✓ Saved to stocks-data.json")
print("\nSample data:")
for stock in stocks[:5]:
    print(f"  {stock['code']:12} | Price: ${stock.get('price', 'N/A'):>10} | "
          f"Change: ${stock.get('changeAmount', 'N/A'):>8} | "
          f"Daily%: {stock.get('dailyChangePct', 'N/A')}%")
