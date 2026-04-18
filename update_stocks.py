"""
Unified Stock Data Fetcher - Main Entry Point
Supports both Yahoo Finance (default) and FXCM (alternative)
"""

import sys
import json
from datetime import datetime


def print_header():
    """Print application header"""
    print("=" * 60)
    print("Global Stocks Dashboard - Data Fetcher")
    print("=" * 60)
    print()
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def check_yahoo_finance():
    """Check if Yahoo Finance dependencies are available"""
    try:
        import yfinance
        import pandas
        return True
    except ImportError:
        return False


def check_fxcm():
    """Check if FXCM dependencies are available"""
    try:
        # Check Python version first
        if sys.version_info >= (3, 8):
            return False
        
        from forexconnect import ForexConnect
        return True
    except (ImportError, Exception):
        return False


def run_yahoo_finance():
    """Run Yahoo Finance data fetcher"""
    print("📊 Using Yahoo Finance API")
    print("-" * 60)
    print()
    
    try:
        from fetch_yahoo_data import update_stock_data_with_yahoo, generate_sample_data
        
        # Show progress
        def progress_callback(current, total, message):
            percent = (current / total * 100) if total > 0 else 0
            print(f"\r  Progress: [{current}/{total}] {percent:.1f}% - {message}", end='', flush=True)
        
        print("Fetching real-time stock data from Yahoo Finance...")
        print()
        
        success = update_stock_data_with_yahoo(progress_callback=progress_callback)
        
        print()  # New line after progress
        print()
        
        if success:
            print("✅ Successfully updated stock data!")
            print()
            print("Next steps:")
            print("  1. Start the web server: python server.py")
            print("  2. Open browser: http://localhost:8000")
            print("  3. Refresh to see updated data")
        else:
            print("⚠️  Failed to fetch data from Yahoo Finance.")
            print()
            choice = input("Generate sample data instead? (y/n): ").strip().lower()
            if choice == 'y':
                generate_sample_data()
                print()
                print("✅ Sample data generated!")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def run_fxcm():
    """Run FXCM data fetcher"""
    print("🏦 Using FXCM Forex Connect API")
    print("-" * 60)
    print()
    
    # Check Python version
    if sys.version_info >= (3, 8):
        print("❌ ERROR: FXCM Forex Connect requires Python 3.5, 3.6, or 3.7")
        print(f"   Current Python version: {sys.version}")
        print()
        print("Please run with Python 3.7:")
        print("  py -3.7 update_stocks.py --fxcm")
        return False
    
    try:
        from fetch_fxcm_data import update_json_with_trading_data
        update_json_with_trading_data()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def show_status():
    """Show current data status"""
    print("📈 Current Data Status")
    print("-" * 60)
    print()
    
    try:
        with open('stocks-data.json', 'r') as f:
            data = json.load(f)
        
        total = len(data)
        with_real_data = sum(1 for stock in data if stock.get('price') is not None)
        with_sample_data = total - with_real_data
        
        print(f"Total stocks: {total}")
        print(f"With real data: {with_real_data}")
        print(f"With sample data: {with_sample_data}")
        print()
        
        if with_real_data > 0:
            print("Sample stocks with real data:")
            count = 0
            for stock in data:
                if stock.get('price') and count < 5:
                    print(f"  {stock['code']:12} | ${stock['price']:10.2f} | {stock['name']}")
                    count += 1
        print()
        
    except FileNotFoundError:
        print("❌ stocks-data.json not found")
        print("   Run convert_to_json.py first to create it")
        print()
    except Exception as e:
        print(f"❌ Error reading data: {e}")
        print()


def main():
    """Main function"""
    print_header()
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    if '--status' in args:
        show_status()
        return
    
    if '--fxcm' in args:
        # Use FXCM
        if check_fxcm():
            run_fxcm()
        else:
            print("❌ FXCM Forex Connect API is not available")
            print()
            print("Requirements:")
            print("  1. Python 3.5, 3.6, or 3.7")
            print("  2. forexconnect package installed")
            print("  3. Valid FXCM credentials in fxcm_config.py")
            print()
            print("Install forexconnect:")
            print("  py -3.7 -m pip install forexconnect")
            print()
            print("Switching to Yahoo Finance...")
            print()
            if check_yahoo_finance():
                run_yahoo_finance()
            else:
                print("❌ Yahoo Finance also not available")
                print("Install with: pip install yfinance pandas")
        return
    
    # Default: Use Yahoo Finance
    if check_yahoo_finance():
        run_yahoo_finance()
    elif check_fxcm():
        print("⚠️  Yahoo Finance not available, using FXCM instead")
        print()
        run_fxcm()
    else:
        print("❌ No data source available!")
        print()
        print("Options:")
        print()
        print("1. Yahoo Finance (Recommended - Easiest):")
        print("   pip install yfinance pandas")
        print()
        print("2. FXCM Forex Connect (Alternative):")
        print("   - Requires Python 3.7")
        print("   - py -3.7 -m pip install forexconnect")
        print("   - Valid FXCM credentials required")
        print()
        
        choice = input("Generate sample data for now? (y/n): ").strip().lower()
        if choice == 'y':
            try:
                from fetch_yahoo_data import generate_sample_data
                generate_sample_data()
                print()
                print("✅ Sample data generated!")
            except:
                print("❌ Could not generate sample data")


if __name__ == "__main__":
    main()
