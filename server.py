import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8001
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Allow port reuse
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"Starting server at http://localhost:{PORT}")
print("Press Ctrl+C to stop the server")
print("")

try:
    with ReusableTCPServer(("", PORT), Handler) as httpd:
        # Open the browser automatically
        webbrowser.open(f'http://localhost:{PORT}')
        print("Browser opened automatically!")
        print("")
        print("Dashboard is running...")
        print("Keep this window open while using the dashboard.")
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
