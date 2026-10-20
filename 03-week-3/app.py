"""
Standalone HTTP Server for SlothDigest AI (Week 3)
Pure Python standard library implementation.
"""

import http.server
import socketserver
import json
import os
from urllib.parse import urlparse
from sloth_engine import SlothDigestEngine

PORT = int(os.environ.get("PORT", 8083))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

engine = SlothDigestEngine()

class SlothDigestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self._serve_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
            return

        if path == "/api/health":
            self._send_json({"status": "healthy", "service": "sloth-digest-ai"})
            return

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

        if path in ("/api/triage/distill", "api/triage/distill"):
            text = payload.get("text", "")
            alias = payload.get("user_alias", "me")
            res = engine.distill_thread(text, alias)
            self._send_json(res)
            return

        if path in ("/api/winddown/plan", "api/winddown/plan"):
            ftype = payload.get("fatigue_type", "screen_eye_strain")
            mins = payload.get("minutes", 20)
            res = engine.generate_wind_down(mins, ftype)
            self._send_json(res)
            return

        if path in ("/api/task/simplify", "api/task/simplify"):
            task = payload.get("task", "")
            res = engine.simplify_task(task)
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
    with socketserver.TCPServer(("", PORT), SlothDigestHandler) as httpd:
        print(f"[*] SlothDigest AI Server running on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()
