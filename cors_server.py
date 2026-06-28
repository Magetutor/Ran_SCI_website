#!/usr/bin/env python3
"""HTTP server with CORS headers for vitessce.io cross-origin data loading."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

PORT = 8899
DIR = os.path.dirname(os.path.abspath(__file__))

class CORSHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

print(f'Serving {DIR} on port {PORT} with CORS')
HTTPServer(('0.0.0.0', PORT), CORSHandler).serve_forever()
