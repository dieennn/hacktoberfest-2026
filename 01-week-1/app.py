"""
Standalone HTTP Server for TrailFlora & Garden AI (Week 1)
Pure Python standard library implementation.
"""

import http.server
import socketserver
import json
import os
from urllib.parse import urlparse
from engine import TrailFloraEngine, PLANT_TAXONOMY, GARDEN_SCHEDULES

PORT = int(os.environ.get("PORT", 8081))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

engine = TrailFloraEngine()

class TrailFloraHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self._serve_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
            return

        if path == "/api/health":
            self._send_json({"status": "healthy", "service": "trail-flora-ai"})
            return

        # Serve static assets
        file_path = os.path.join(STATIC_DIR, path.lstrip("/"))
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self._serve_file(file_path, "application/octet-stream")
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if path in ("/api/plant/scan", "api/plant/scan"):
            query = payload.get("query", "")
            res = engine.identify_plant(query)
            self._send_json(res)
            return

        if path in ("/api/garden/plan", "api/garden/plan"):
            zone = payload.get("zone", "zone_5_6")
            temp_c = payload.get("temp_c", 10)
            res = engine.plan_garden(zone, temp_c)
            self._send_json(res)
            return

        if path in ("/api/grass/scout", "api/grass/scout"):
            temp_c = payload.get("temp_c", 18)
            cloud_pct = payload.get("cloud_pct", 20)
            duration = payload.get("duration_mins", 45)
            res = engine.scout_outdoor_window(cloud_pct, temp_c, duration)
            self._send_json(res)
            return

        self.send_response(404)
        self.end_headers()

    def _send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _serve_file(self, path, content_type):
        if path.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        elif path.endswith(".css"):
            content_type = "text/css"
        elif path.endswith(".js"):
            content_type = "application/javascript"

        with open(path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TrailFloraHandler) as httpd:
        print(f"[*] TrailFlora AI Server running on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()
