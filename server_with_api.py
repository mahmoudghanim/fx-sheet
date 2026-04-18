"""
Enhanced server with stock management API
Supports adding, removing, and updating stocks
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import json
from urllib.parse import urlparse, parse_qs

PORT = 8001
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Allow port reuse
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class StockHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_POST(self):
        """Handle POST requests for stock management"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/save-stocks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                stocks_data = json.loads(post_data.decode('utf-8'))
                
                # Save to file
                save_path = os.path.join(DIRECTORY, 'stocks-data.json')
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(stocks_data, f, indent=2, ensure_ascii=False)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'status': 'success', 'message': 'Stocks saved successfully'})
                self.wfile.write(response.encode('utf-8'))
                
                print(f"✓ Saved {len(stocks_data)} stocks to stocks-data.json")
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'status': 'error', 'message': str(e)})
                self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print(f"Starting server at http://localhost:{PORT}")
print("Press Ctrl+C to stop the server")
print("")

try:
    with ReusableTCPServer(("", PORT), StockHandler) as httpd:
        # Open the browser automatically
        webbrowser.open(f'http://localhost:{PORT}')
        print("Browser opened automatically!")
        print("")
        print("Dashboard is running...")
        print("Keep this window open while using the dashboard.")
        print("")
        print("Stock Management API:")
        print("  POST /api/save-stocks - Save stock data")
        httpd.serve_forever()
except OSError as e:
    if "Only one usage" in str(e):
        print(f"ERROR: Port {PORT} is already in use!")
        print("Please close any other instances of the dashboard.")
        print("")
        print("To fix this:")
        print("1. Close all command windows running the dashboard")
        print("2. Or change the PORT number in server.py")
    else:
        print(f"ERROR: {e}")
    sys.exit(1)
