#!/usr/bin/env python3
"""
Simple HTTP server to serve the built React app
"""
import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="dist", **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Handle SPA routing - serve index.html for all routes
        if self.path != '/' and not self.path.startswith('/assets'):
            self.path = '/'
        return super().do_GET()

if __name__ == "__main__":
    # Change to the directory containing this script
    os.chdir(Path(__file__).parent)
    
    # Check if dist directory exists
    if not os.path.exists('dist'):
        print("❌ Dist directory not found. Please run 'npm run build' first.")
        sys.exit(1)
    
    print(f"🚀 Starting server on http://localhost:{PORT}")
    print(f"📁 Serving files from: {os.path.abspath('dist')}")
    print("📡 Backend API URL: https://web-production-92856.up.railway.app")
    print("💡 Press Ctrl+C to stop the server")
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            # Open browser automatically
            webbrowser.open(f'http://localhost:{PORT}')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
