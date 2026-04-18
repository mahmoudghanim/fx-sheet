"""
Yahoo Finance Stock Data Fetcher
Fetches real-time stock data from Yahoo Finance API
Supports batch processing with progress indication
"""

import json
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Try to import yfinance
try:
    import yfinance as yf
    import pandas as pd
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("✗ yfinance package not installed!")
    print("Install with: pip install yfinance pandas")
    sys.exit(1)

# Import configuration
try:
    from fxcm_config import SAVE_TO_FILE, LOG_FILE
except ImportError:
    SAVE_TO_FILE = "stocks-data.json"
    LOG_FILE = "yahoo_fetch.log"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def fxcm_to_yahoo_symbol(fxcm_symbol):
    """
    Convert FXCM symbol format to Yahoo Finance format
    
    Examples:
    - ABBV.us -> ABBV
    - ABN.nl -> ABN.AS (Amsterdam)
    - ADS.de -> ADS.DE (Germany)
    - AAPL.us -> AAPL
    - 7203.jp -> 7203.T (Tokyo)
    """
    if not fxcm_symbol or '.' not in fxcm_symbol:
        return fxcm_symbol
    
    parts = fxcm_symbol.split('.')
    base_symbol = parts[0]
    country_code = parts[1].lower() if len(parts) > 1 else ''
    
    # Country/exchange mapping
    exchange_map = {
        'us': '',           # US stocks - no suffix needed
        'gb': '.L',         # London
        'de': '.DE',        # Germany (XETRA)
        'fr': '.PA',        # Paris (Euronext)
        'nl': '.AS',        # Amsterdam
        'es': '.MC',        # Madrid
        'it': '.MI',        # Milan
        'ch': '.SW',        # Switzerland
        'se': '.ST',        # Stockholm
        'dk': '.CO',        # Copenhagen
        'no': '.OL',        # Oslo
        'jp': '.T',         # Tokyo
        'hk': '.HK',        # Hong Kong
        'cn': '.SS',        # Shanghai
        'au': '.AX',        # Australia
        'ca': '.TO',        # Toronto
        'br': '.SA',        # Brazil
        'in': '.NS',        # India (NSE)
        'kr': '.KS',        # Korea
        'sg': '.SI',        # Singapore
        'mx': '.MX',        # Mexico
    }
    
    suffix = exchange_map.get(country_code, '')
    yahoo_symbol = f"{base_symbol}{suffix}"
    
    return yahoo_symbol


def fetch_stock_batch(symbols, max_retries=2):
    """
    Fetch data for a batch of stocks from Yahoo Finance
    
    Args:
        symbols: List of Yahoo Finance symbols
        max_retries: Number of retries for failed requests
    
    Returns:
        Dictionary with symbol -> data mapping
    """
    batch_data = {}
    
    try:
        # Fetch data for all symbols in batch
        tickers = yf.Tickers(' '.join(symbols))
        
        for symbol in symbols:
            try:
                ticker = tickers.tickers[symbol]
                info = ticker.info
                
                # Extract relevant data
                data = {
                    'currentPrice': info.get('currentPrice'),
                    'regularMarketVolume': info.get('regularMarketVolume'),
                    'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow'),
                    'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh'),
                    'regularMarketChange': info.get('regularMarketChange'),
                    'regularMarketChangePercent': info.get('regularMarketChangePercent'),
                    'marketCap': info.get('marketCap'),
                    'previousClose': info.get('previousClose'),
                    'open': info.get('open'),
                    'dayHigh': info.get('dayHigh'),
                    'dayLow': info.get('dayLow'),
                    'sector': info.get('sector'),
                    'industry': info.get('industry'),
                    'currency': info.get('currency'),
                }
                
                batch_data[symbol] = data
                
            except Exception as e:
                logger.debug(f"Could not fetch data for {symbol}: {e}")
                batch_data[symbol] = None
    
    except Exception as e:
        logger.error(f"Batch fetch error: {e}")
    
    return batch_data


def update_stock_data_with_yahoo(progress_callback=None):
    """
    Update stocks-data.json with real data from Yahoo Finance
    
    Args:
        progress_callback: Optional callback function for progress updates
                          Signature: callback(current, total, message)
    """
    logger.info("=" * 60)
    logger.info("Starting Yahoo Finance data fetch...")
    logger.info("=" * 60)
    
    # Load existing stock data
    try:
        with open(SAVE_TO_FILE, 'r') as f:
            stocks_data = json.load(f)
        logger.info(f"✓ Loaded {len(stocks_data)} stocks from {SAVE_TO_FILE}")
    except FileNotFoundError:
        logger.error(f"✗ {SAVE_TO_FILE} not found")
        return False
    except json.JSONDecodeError:
        logger.error(f"✗ {SAVE_TO_FILE} contains invalid JSON")
        return False
    
    # Convert FXCM symbols to Yahoo Finance symbols
    logger.info("Converting symbols to Yahoo Finance format...")
    symbol_mapping = []
    for stock in stocks_data:
        fxcm_symbol = stock.get('code', '')
        yahoo_symbol = fxcm_to_yahoo_symbol(fxcm_symbol)
        symbol_mapping.append({
            'stock': stock,
            'fxcm_symbol': fxcm_symbol,
            'yahoo_symbol': yahoo_symbol
        })
    
    total_stocks = len(symbol_mapping)
    logger.info(f"✓ Prepared {total_stocks} symbols for fetching")
    
    # Process in batches
    batch_size = 50  # Yahoo Finance handles 50 stocks per batch well
    batches = [symbol_mapping[i:i + batch_size] for i in range(0, total_stocks, batch_size)]
    
    updated_count = 0
    failed_count = 0
    total_batches = len(batches)
    
    logger.info(f"Processing {total_batches} batches of {batch_size} stocks...")
    logger.info("")
    
    # Fetch data batch by batch
    for batch_idx, batch in enumerate(batches, 1):
        batch_symbols = [item['yahoo_symbol'] for item in batch]
        
        # Progress update
        progress_msg = f"Batch {batch_idx}/{total_batches} ({batch_idx * batch_size}/{total_stocks} stocks)"
        logger.info(progress_msg)
        
        if progress_callback:
            progress_callback(
                (batch_idx - 1) * batch_size,
                total_stocks,
                progress_msg
            )
        
        # Fetch batch data with retry logic
        batch_data = None
        for attempt in range(3):  # Max 3 attempts
            try:
                batch_data = fetch_stock_batch(batch_symbols)
                if batch_data:
                    break
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2)  # Wait before retry
        
        if not batch_data:
            logger.warning(f"⚠️  Failed to fetch batch {batch_idx}")
            failed_count += len(batch)
            continue
        
        # Update stock data
        for item in batch:
            fxcm_symbol = item['fxcm_symbol']
            yahoo_symbol = item['yahoo_symbol']
            stock = item['stock']
            
            data = batch_data.get(yahoo_symbol)
            
            if data and data.get('currentPrice'):
                # Update stock with real data
                stock['price'] = round(data['currentPrice'], 2) if data['currentPrice'] else None
                stock['volume'] = data['regularMarketVolume'] if data['regularMarketVolume'] else None
                stock['week52Low'] = round(data['fiftyTwoWeekLow'], 2) if data['fiftyTwoWeekLow'] else None
                stock['week52High'] = round(data['fiftyTwoWeekHigh'], 2) if data['fiftyTwoWeekHigh'] else None
                stock['changeAmount'] = round(data['regularMarketChange'], 2) if data['regularMarketChange'] else None
                
                # Convert change percent
                if data['regularMarketChangePercent']:
                    stock['change52W'] = round(data['regularMarketChangePercent'], 2)
                else:
                    stock['change52W'] = None
                
                # Add industry and sector
                stock['industry'] = data.get('industry')
                stock['sector'] = data.get('sector')
                stock['currency'] = data.get('currency')
                
                updated_count += 1
            else:
                failed_count += 1
                logger.debug(f"✗ No data for {fxcm_symbol} ({yahoo_symbol})")
        
        # Rate limiting - be respectful to Yahoo Finance API
        if batch_idx < total_batches:
            time.sleep(1)  # 1 second delay between batches
    
    # Save updated data
    logger.info("")
    logger.info("Saving updated data...")
    with open(SAVE_TO_FILE, 'w') as f:
        json.dump(stocks_data, f, indent=2)
    
    # Final progress update
    if progress_callback:
        progress_callback(total_stocks, total_stocks, "Complete!")
    
    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("FETCH COMPLETE!")
    logger.info("=" * 60)
    logger.info(f"Total stocks: {total_stocks}")
    logger.info(f"Successfully updated: {updated_count}")
    logger.info(f"Failed/No data: {failed_count}")
    logger.info(f"Success rate: {(updated_count / total_stocks * 100):.1f}%")
    logger.info(f"Data saved to: {SAVE_TO_FILE}")
    logger.info("=" * 60)
    
    # Show sample
    logger.info("")
    logger.info("Sample updated data:")
    sample_count = 0
    for stock in stocks_data:
        if stock.get('price') and sample_count < 10:
            logger.info(
                f"  {stock['code']:12} | ${stock['price']:10.2f} | "
                f"Volume: {str(stock.get('volume', 'N/A')):>12} | "
                f"52W Change: {str(stock.get('change52W', 'N/A')):>8}%"
            )
            sample_count += 1
    
    return updated_count > 0


def generate_sample_data():
    """Generate sample trading data for demonstration (fallback)"""
    import random
    
    logger.info("Generating sample trading data for demonstration...")
    
    try:
        with open(SAVE_TO_FILE, 'r') as f:
            stocks_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"✗ {SAVE_TO_FILE} not found")
        return
    
    for i, stock in enumerate(stocks_data, 1):
        base_price = random.uniform(10, 500)
        stock['price'] = round(base_price, 2)
        stock['volume'] = random.randint(100000, 50000000)
        stock['week52Low'] = round(base_price * random.uniform(0.6, 0.85), 2)
        stock['week52High'] = round(base_price * random.uniform(1.15, 1.5), 2)
        stock['changeAmount'] = round(random.uniform(-10, 10), 2)
        stock['change52W'] = round(random.uniform(-30, 80), 2)
        
        if i % 100 == 0:
            logger.info(f"  Generated {i}/{len(stocks_data)} stocks...")
    
    with open(SAVE_TO_FILE, 'w') as f:
        json.dump(stocks_data, f, indent=2)
    
    logger.info(f"\n✓ Generated sample data for {len(stocks_data)} stocks")


if __name__ == "__main__":
    print("=" * 60)
    print("Yahoo Finance Stock Data Fetcher")
    print("=" * 60)
    print()
    
    if not YFINANCE_AVAILABLE:
        print("✗ yfinance not installed!")
        print("Install with: pip install yfinance pandas")
        sys.exit(1)
    
    # Fetch real data
    success = update_stock_data_with_yahoo()
    
    if not success:
        print()
        print("Failed to fetch data from Yahoo Finance.")
        choice = input("Generate sample data instead? (y/n): ").strip().lower()
        if choice == 'y':
            generate_sample_data()
    
    print()
    print("Done! Refresh your dashboard to see updated data.")
