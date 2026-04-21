"""
Categorize stocks into trading sessions: Asia, Europe, America
Based on country and exchange information
"""
import json

print("Categorizing stocks into trading sessions...")

# Load existing data
with open('stocks-data.json', 'r') as f:
    stocks = json.load(f)

print(f"Loaded {len(stocks)} stocks")

# Trading session mapping based on country/exchange
def get_trading_session(country, exchange, code):
    """Determine trading session based on country and exchange"""
    
    # America Session
    america_countries = [
        'United States', 'Canada', 'Brazil', 'Mexico', 'Argentina', 
        'Chile', 'Colombia', 'Peru'
    ]
    america_exchanges = ['NYSE', 'NASDAQ', 'TSX', 'BMV']
    
    # Europe Session  
    europe_countries = [
        'United Kingdom', 'Germany', 'France', 'Netherlands', 'Spain',
        'Italy', 'Switzerland', 'Sweden', 'Denmark', 'Norway',
        'Finland', 'Belgium', 'Austria', 'Portugal', 'Ireland',
        'Greece', 'Poland', 'Czech Republic', 'Hungary', 'Russia',
        'Turkey', 'Luxembourg', 'Iceland'
    ]
    europe_exchanges = ['LSE', 'XETR', 'EURONEXT', 'SIX', 'OMX', 'BME', 'BIT']
    
    # Asia Session
    asia_countries = [
        'Japan', 'China', 'Hong Kong', 'South Korea', 'Singapore',
        'India', 'Australia', 'New Zealand', 'Taiwan', 'Thailand',
        'Malaysia', 'Indonesia', 'Philippines', 'Vietnam', 'Pakistan',
        'Bangladesh', 'Sri Lanka'
    ]
    asia_exchanges = ['TSE', 'HKEX', 'SSE', 'SZSE', 'KRX', 'SGX', 'ASX', 'BSE', 'NSE']
    
    country_str = str(country).lower() if country else ''
    exchange_str = str(exchange).upper() if exchange else ''
    code_str = str(code).lower() if code else ''
    
    # Check America
    for c in america_countries:
        if c.lower() in country_str:
            return 'America'
    for e in america_exchanges:
        if e.lower() in exchange_str.lower():
            return 'America'
    
    # Check Europe
    for c in europe_countries:
        if c.lower() in country_str:
            return 'Europe'
    for e in europe_exchanges:
        if e.lower() in exchange_str.lower():
            return 'Europe'
    
    # Check Asia
    for c in asia_countries:
        if c.lower() in country_str:
            return 'Asia'
    for e in asia_exchanges:
        if e.lower() in exchange_str.lower():
            return 'Asia'
    
    # Fallback: Check country code in stock symbol
    if '.us' in code_str or '.ca' in code_str or '.mx' in code_str or '.br' in code_str:
        return 'America'
    if '.jp' in code_str or '.hk' in code_str or '.cn' in code_str or '.kr' in code_str or '.sg' in code_str or '.in' in code_str or '.au' in code_str:
        return 'Asia'
    if '.gb' in code_str or '.de' in code_str or '.fr' in code_str or '.nl' in code_str or '.es' in code_str or '.it' in code_str or '.ch' in code_str:
        return 'Europe'
    
    # Default to America if unknown
    return 'America'

# Add trading session to each stock
session_counts = {'Asia': 0, 'Europe': 0, 'America': 0}

for stock in stocks:
    session = get_trading_session(
        stock.get('country', ''),
        stock.get('exchange', ''),
        stock.get('code', '')
    )
    stock['session'] = session
    session_counts[session] = session_counts.get(session, 0) + 1

# Save updated data
with open('stocks-data.json', 'w') as f:
    json.dump(stocks, f, indent=2)

print(f"\n✓ Categorized all stocks into trading sessions:")
print(f"  Asia:    {session_counts['Asia']} stocks")
print(f"  Europe:  {session_counts['Europe']} stocks")
print(f"  America: {session_counts['America']} stocks")
print(f"\n✓ Saved to stocks-data.json")

print("\nSample data:")
for stock in stocks[:10]:
    print(f"  {stock['code']:12} | {stock.get('country', 'N/A'):20} | Session: {stock.get('session', 'N/A')}")
