"""
Standalone HTTP Server for HustleLedger AI (Week 2)
Pure Python standard library implementation.
"""

import http.server
import socketserver
import json
import os
from urllib.parse import urlparse
from engine import HustleLedgerEngine

PORT = int(os.environ.get("PORT", 8082))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

engine = HustleLedgerEngine()

class HustleLedgerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self._serve_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
            return

        if path == "/api/health":
            self._send_json({"status": "healthy", "service": "hustle-ledger-ai"})
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

        if path in ("/api/expense/categorize", "api/expense/categorize"):
            desc = payload.get("description", "")
            amt = float(payload.get("amount", 0.0))
            res = engine.categorize_expense(desc, amt)
            self._send_json(res)
            return

        if path in ("/api/invoice/generate", "api/invoice/generate"):
            client = payload.get("client", "")
            project = payload.get("project", "")
            items = payload.get("items", [])
            res = engine.generate_invoice(client, project, items)
            self._send_json(res)
            return

        if path in ("/api/comms/draft", "api/comms/draft"):
            comm_type = payload.get("comm_type", "overdue_reminder")
            client = payload.get("client_name", "")
            amt = float(payload.get("amount", 0.0))
            ctx = payload.get("context", "")
            draft = engine.draft_client_communication(comm_type, client, amt, ctx)
            self._send_json({"draft": draft})
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
    with socketserver.TCPServer(("", PORT), HustleLedgerHandler) as httpd:
        print(f"[*] HustleLedger AI Server running on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()
