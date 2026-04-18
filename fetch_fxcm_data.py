"""
FXCM Stock Data Fetcher - Using Forex Connect API
This script fetches real-time stock data from FXCM using Forex Connect API

Requirements:
    pip install forexconnect pandas
    Note: forexconnect works with Python 3.5, 3.6, 3.7

For Python 3.8+, you must use Python 3.7 specifically:
    py -3.7 fetch_fxcm_data.py

To get your FXCM credentials:
    1. Go to https://www.fxcm.com/
    2. Create a demo or live account
    3. Use your Trading Station login credentials
    4. Edit fxcm_config.py and add your credentials
"""

import json
import sys
import logging
from datetime import datetime

# Try to import configuration
try:
    from fxcm_config import (
        FXCM_USERNAME,
        FXCM_PASSWORD,
        FXCM_ACCOUNT_TYPE,
        FXCM_URL,
        SAVE_TO_FILE,
        LOG_FILE,
        UPDATE_INTERVAL_MINUTES,
        PRIORITY_STOCKS
    )
    CONFIG_LOADED = True
except ImportError:
    print("⚠️  Configuration file not found!")
    print("Please create fxcm_config.py with your FXCM credentials.")
    sys.exit(1)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def fetch_data_with_forex_connect():
    """
    Fetch market data using FXCM Forex Connect API
    Documentation: https://fxcodebase.com/wiki/index.php/Category:ForexConnect
    """
    
    logger.info("Starting FXCM Forex Connect API data fetch...")
    
    # Check Python version
    if sys.version_info >= (3, 8):
        logger.error("ERROR: Forex Connect API requires Python 3.5, 3.6, or 3.7")
        logger.error(f"Current Python version: {sys.version}")
        logger.error("Please run with Python 3.7: py -3.7 fetch_fxcm_data.py")
        return False
    
    # Try to import forexconnect
    try:
        from forexconnect import ForexConnect
        logger.info("✓ forexconnect package loaded successfully")
    except ImportError:
        logger.error("✗ forexconnect package not installed")
        logger.error("Install with: py -3.7 -m pip install forexconnect")
        return False
    
    # Validate credentials
    if FXCM_USERNAME == "YOUR_USERNAME_HERE":
        logger.error("✗ FXCM credentials not configured!")
        logger.error("Please edit fxcm_config.py and add your credentials")
        return False
    
    try:
        # Connect to FXCM
        logger.info(f"Connecting to FXCM ({FXCM_ACCOUNT_TYPE} account)...")
        logger.info(f"Username: {FXCM_USERNAME}")
        logger.info(f"URL: {FXCM_URL}")
        
        session = ForexConnect()
        session.login(FXCM_USERNAME, FXCM_PASSWORD, FXCM_ACCOUNT_TYPE, FXCM_URL)
        
        logger.info("✓ Successfully connected to FXCM!")
        
        # Fetch instruments
        logger.info("Fetching available instruments...")
        instruments = session.get_instruments()
        logger.info(f"Found {len(instruments)} instruments")
        
        # Fetch prices for each instrument
        stock_updates = []
        for i, instrument in enumerate(instruments, 1):
            try:
                # Get current price
                price = session.get_price(instrument)
                stock_updates.append({
                    'symbol': instrument,
                    'bid': price['bid'],
                    'ask': price['ask'],
                    'timestamp': datetime.now().isoformat()
                })
                
                if i % 50 == 0:
                    logger.info(f"Fetched {i}/{len(instruments)} instruments...")
                    
            except Exception as e:
                logger.warning(f"Could not fetch price for {instrument}: {e}")
                continue
        
        # Logout
        session.logout()
        logger.info("✓ Disconnected from FXCM")
        
        # Update JSON file
        update_stock_data(stock_updates)
        
        logger.info(f"✓ Successfully updated {len(stock_updates)} stocks")
        return True
        
    except Exception as e:
        logger.error(f"✗ Error connecting to FXCM: {str(e)}")
        logger.error("Please check your credentials and internet connection")
        return False


def update_stock_data(stock_updates):
    """
    Update the stocks-data.json file with new price data
    """
    logger.info("Updating stock data file...")
    
    try:
        with open(SAVE_TO_FILE, 'r') as f:
            stocks_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"✗ {SAVE_TO_FILE} not found")
        return
    
    # Create a lookup dictionary for quick updates
    price_lookup = {update['symbol']: update for update in stock_updates}
    
    # Update existing stocks
    updated_count = 0
    for stock in stocks_data:
        symbol = stock.get('code', '')
        
        # Try different symbol formats
        for fmt in [symbol, symbol.replace('.', '/'), f"{symbol.split('.')[0]}"]:
            if fmt in price_lookup:
                price_data = price_lookup[fmt]
                stock['price'] = round((price_data['bid'] + price_data['ask']) / 2, 2)
                # You can add more fields here as needed
                updated_count += 1
                break
    
    # Save updated data
    with open(SAVE_TO_FILE, 'w') as f:
        json.dump(stocks_data, f, indent=2)
    
    logger.info(f"✓ Updated {updated_count} stocks in {SAVE_TO_FILE}")


def generate_sample_trading_data():
    """
    Generate realistic sample trading data for demonstration
    """
    import random
    
    logger.info("Generating sample trading data for demonstration...")
    
    # Read existing stocks data
    try:
        with open(SAVE_TO_FILE, 'r') as f:
            stocks_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"✗ {SAVE_TO_FILE} not found. Please run convert_to_json.py first.")
        return
    
    # Generate realistic trading data for each stock
    logger.info("Processing stocks...")
    for i, stock in enumerate(stocks_data, 1):
        # Generate realistic data based on stock characteristics
        base_price = random.uniform(10, 500)
        stock['price'] = round(base_price, 2)
        stock['volume'] = random.randint(100000, 50000000)
        stock['week52Low'] = round(base_price * random.uniform(0.6, 0.85), 2)
        stock['week52High'] = round(base_price * random.uniform(1.15, 1.5), 2)
        stock['changeAmount'] = round(random.uniform(-10, 10), 2)
        stock['change52W'] = round(random.uniform(-30, 80), 2)
        
        if i % 100 == 0:
            logger.info(f"  Processed {i}/{len(stocks_data)} stocks...")
    
    # Save updated data
    with open(SAVE_TO_FILE, 'w') as f:
        json.dump(stocks_data, f, indent=2)
    
    logger.info(f"\n✓ Updated {len(stocks_data)} stocks with trading data")
    logger.info(f"✓ Data saved to {SAVE_TO_FILE}")
    
    # Show sample
    logger.info("\nSample data:")
    for stock in stocks_data[:5]:
        logger.info(f"  {stock['code']:10} | ${stock['price']:8.2f} | Volume: {stock['volume']:>10,} | 52W Change: {stock['change52W']:>6.2f}%")


def create_python37_env_instructions():
    """Print instructions for creating Python 3.7 environment"""
    logger.info("="*60)
    logger.info("Creating Python 3.7 Environment")
    logger.info("="*60)
    logger.info("""
Option 1 - Using setup script (Easiest):
  Run: setup_fxcm.bat

Option 2 - Manual installation:
  1. Download Python 3.7.9:
     https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe
  
  2. Install and check "Add to PATH"
  
  3. Install forexconnect:
     py -3.7 -m pip install forexconnect
  
  4. Run the script:
     py -3.7 fetch_fxcm_data.py
""")


def update_json_with_trading_data():
    """Main function to update stock data"""
    print("=" * 60)
    print("FXCM Stock Data Updater - Forex Connect API")
    print("=" * 60)
    print()
    
    # Check Python version
    if sys.version_info >= (3, 8):
        print("⚠️  WARNING: You're using Python " + ".".join(map(str, sys.version_info[:3])))
        print("   Forex Connect API requires Python 3.5, 3.6, or 3.7")
        print()
        print("Please run with Python 3.7:")
        print("   py -3.7 fetch_fxcm_data.py")
        print()
        print("If you don't have Python 3.7 installed:")
        print("   1. Run setup_fxcm.bat to install it")
        print("   2. Download from: https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe")
        print()
        return
    
    if not CONFIG_LOADED or FXCM_USERNAME == "YOUR_USERNAME_HERE":
        print("⚠️  FXCM credentials not configured!")
        print()
        print("Please edit fxcm_config.py and add:")
        print("  - FXCM_USERNAME (your Trading Station username)")
        print("  - FXCM_PASSWORD (your Trading Station password)")
        print("  - FXCM_ACCOUNT_TYPE (Demo or Real)")
        print()
        print("Don't have an FXCM account?")
        print("  1. Go to https://www.fxcm.com/")
        print("  2. Create a FREE demo account")
        print("  3. Use those credentials")
        print()
        
        choice = input("Generate sample data for now? (y/n): ").strip().lower()
        if choice == 'y':
            generate_sample_trading_data()
        return
    
    # Fetch real data from FXCM
    success = fetch_data_with_forex_connect()
    
    if not success:
        print()
        print("Failed to fetch data from FXCM.")
        print("Would you like to generate sample data instead?")
        choice = input("Generate sample data? (y/n): ").strip().lower()
        if choice == 'y':
            generate_sample_trading_data()


if __name__ == "__main__":
    update_json_with_trading_data()
