import pandas as pd
import json

# Read the Excel file
df = pd.read_excel('Listing.xlsx')

# Convert to list of dictionaries with the structure needed for the web page
stocks_data = []

for index, row in df.iterrows():
    stock = {
        'code': row['FXCM Symbol'],
        'name': row['Company'],
        'country': row['Country'],
        'price': None,  # Will be added later when you provide trading data
        'volume': None,
        'week52Low': None,
        'week52High': None,
        'changeAmount': None,
        'change52W': None,
        'product': row.get('Product', ''),
        'exchange': row.get('Exchange', '')
    }
    stocks_data.append(stock)

# Write to JSON file
with open('stocks-data.json', 'w') as f:
    json.dump(stocks_data, f, indent=2)

print(f"Successfully converted {len(stocks_data)} stocks to JSON format")
print("JSON file created: stocks-data.json")
