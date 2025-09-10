#!/usr/bin/env python3
"""
Simple HTTP server for the transit map
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class TransitHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    """Start the HTTP server"""
    with socketserver.TCPServer(("", PORT), TransitHTTPRequestHandler) as httpd:
        print(f"🌐 Starting transit map server on port {PORT}")
        print(f"📍 Map URL: http://localhost:{PORT}/map.html")
        print(f"🗂️  Serving files from: {os.getcwd()}")
        print(f"📊 Data files available:")
        
        # List available data files
        data_files = sorted(Path('.').glob('transit_locations_*.json'))
        for file in data_files:
            print(f"   - {file.name}")
        
        print(f"\n🚀 Opening map in browser...")
        webbrowser.open(f'http://localhost:{PORT}/map.html')
        
        print(f"💡 Press Ctrl+C to stop the server")
        print(f"🔄 Refresh the page to load new data after running location_tracker.py")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped")

if __name__ == "__main__":
    start_server()
