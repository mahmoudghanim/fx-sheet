import json

with open('stocks-data.json', 'r') as f:
    data = json.load(f)

# Check first 5 stocks
for stock in data[:5]:
    print(f"Code: {stock['code']}")
    print(f"Industry: {stock.get('industry', 'N/A')}")
    print(f"Sector: {stock.get('sector', 'N/A')}")
    print("-" * 50)
