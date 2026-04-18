"""
Flask version of FX Sheet Dashboard
Better compatibility with shared hosting and platforms like PythonAnywhere, Heroku, etc.
"""

from flask import Flask, send_from_directory, jsonify
import os
import json

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    """Serve the main dashboard"""
    return send_from_directory('.', 'index.html')

@app.route('/stocks-data.json')
def get_stock_data():
    """Serve stock data as JSON"""
    try:
        with open('stocks-data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def serve_static(path):
    """Serve any other static files"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    # For local development
    app.run(host='0.0.0.0', port=8001, debug=True)
