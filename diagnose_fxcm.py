"""
FXCM Connection Diagnostic Tool
This script tests your FXCM connection and provides detailed error information
"""

import sys
from datetime import datetime

print("=" * 60)
print("FXCM Connection Diagnostic Tool")
print("=" * 60)
print()

# Check Python version
print(f"Python Version: {sys.version}")
if sys.version_info >= (3, 8):
    print("⚠️  WARNING: Forex Connect works best with Python 3.7")
    print("   Consider using: py -3.7 diagnose_fxcm.py")
print()

# Try to import forexconnect
try:
    from forexconnect import ForexConnect
    print("✓ forexconnect package imported successfully")
except ImportError as e:
    print(f"✗ ERROR: Cannot import forexconnect: {e}")
    print()
    print("Solution: Install forexconnect with:")
    print("  py -3.7 -m pip install forexconnect")
    sys.exit(1)

# Import configuration
try:
    from fxcm_config import (
        FXCM_USERNAME,
        FXCM_PASSWORD,
        FXCM_ACCOUNT_TYPE,
        FXCM_URL
    )
    print("✓ Configuration loaded successfully")
except ImportError as e:
    print(f"✗ ERROR: Cannot load configuration: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("Connection Test")
print("=" * 60)
print()

# Display configuration (mask password)
print(f"Username: {FXCM_USERNAME}")
print(f"Password: {'*' * len(FXCM_PASSWORD)}")
print(f"Account Type: {FXCM_ACCOUNT_TYPE}")
print(f"URL: {FXCM_URL}")
print()

# Test connection
print("Attempting to connect to FXCM...")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

try:
    session = ForexConnect()
    
    print("Logging in...")
    session.login(FXCM_USERNAME, FXCM_PASSWORD, FXCM_ACCOUNT_TYPE, FXCM_URL)
    
    print("✓ SUCCESS! Connected to FXCM!")
    print()
    
    # Try to get account info
    try:
        accounts = session.get_accounts()
        print(f"✓ Found {len(accounts)} account(s)")
        for acc in accounts:
            print(f"  - Account ID: {acc}")
    except Exception as e:
        print(f"⚠️  Could not retrieve accounts: {e}")
    
    # Try to get instruments
    try:
        print()
        print("Fetching instruments...")
        instruments = session.get_instruments()
        print(f"✓ Found {len(instruments)} instrument(s)")
        
        # Show first 5 instruments
        print()
        print("Sample instruments:")
        for inst in list(instruments)[:5]:
            print(f"  - {inst}")
    except Exception as e:
        print(f"⚠️  Could not retrieve instruments: {e}")
    
    # Logout
    print()
    print("Logging out...")
    session.logout()
    print("✓ Disconnected successfully")
    
    print()
    print("=" * 60)
    print("DIAGNOSIS: Connection is working!")
    print("=" * 60)
    
except Exception as e:
    error_msg = str(e)
    print(f"✗ CONNECTION FAILED!")
    print()
    print(f"Error: {error_msg}")
    print()
    print("=" * 60)
    print("TROUBLESHOOTING GUIDE")
    print("=" * 60)
    print()
    
    # Provide specific troubleshooting based on error
    if "login" in error_msg.lower() or "authentication" in error_msg.lower() or "invalid" in error_msg.lower():
        print("🔑 AUTHENTICATION ERROR")
        print()
        print("Possible causes:")
        print("  1. Incorrect username or password")
        print("  2. Account type mismatch (Demo vs Real)")
        print("  3. Account is locked or disabled")
        print()
        print("Solutions:")
        print("  1. Verify credentials by logging into Trading Station")
        print("     URL: https://tradingstation.fxcm.com/")
        print("  2. Check if account type matches:")
        print("     - Demo account → FXCM_ACCOUNT_TYPE = 'Demo'")
        print("     - Real account → FXCM_ACCOUNT_TYPE = 'Real'")
        print("  3. Contact FXCM support if account is locked")
        print()
        
    elif "connection" in error_msg.lower() or "timeout" in error_msg.lower() or "refused" in error_msg.lower():
        print("🌐 CONNECTION ERROR")
        print()
        print("Possible causes:")
        print("  1. Internet connection issue")
        print("  2. FXCM servers are down")
        print("  3. Firewall blocking connection")
        print("  4. Incorrect URL")
        print()
        print("Solutions:")
        print("  1. Check your internet connection")
        print("  2. Try accessing https://www.fxcm.com/ in browser")
        print("  3. Check FXCM server status: https://status.fxcm.com/")
        print("  4. Verify URL is: www.fxcorporate.com/Hosts.jsp")
        print("  5. Try disabling firewall/antivirus temporarily")
        print()
        
    elif "session" in error_msg.lower():
        print("⚙️  SESSION ERROR")
        print()
        print("Possible causes:")
        print("  1. Multiple sessions open")
        print("  2. Session expired")
        print()
        print("Solutions:")
        print("  1. Wait a few minutes and try again")
        print("  2. Restart your computer")
        print()
        
    else:
        print("❓ UNKNOWN ERROR")
        print()
        print("This is an unexpected error. Please check:")
        print("  1. forexconnect package is properly installed")
        print("  2. Python version is 3.5, 3.6, or 3.7")
        print("  3. FXCM API is still supported (check FXCM website)")
        print()
    
    print("=" * 60)
    print("Alternative: Use Yahoo Finance API")
    print("=" * 60)
    print()
    print("If FXCM connection continues to fail, you can use")
    print("Yahoo Finance as an alternative data source.")
    print()
    print("It's free, doesn't require authentication, and works")
    print("with any Python version.")
    print()
    print("Would you like me to set up Yahoo Finance integration?")
    print()
