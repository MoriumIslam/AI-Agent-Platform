#!/usr/bin/env python3
"""Simple HTTP server to serve the dashboard"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
DASHBOARD_PATH = Path(__file__).parent / "dashboard.html"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html" or self.path == "/dashboard.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            with open(DASHBOARD_PATH, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"🎨 Dashboard Server running on http://0.0.0.0:{PORT}")
        print(f"📍 Open in browser: http://localhost:{PORT}")
        print(f"📍 Or: http://localhost:{PORT}/dashboard.html")
        print(f"\nBackend API: http://localhost:5000")
        print("Press Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
