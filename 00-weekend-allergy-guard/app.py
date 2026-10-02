"""
Allergy & Diet Guard - Local Server
Zero-dependency Python 3 standard library HTTP API & web interface.
"""

import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse
from analyzer import SafetyAnalyzer, ALLERGEN_TAXONOMY, DIETARY_RULES

PORT = int(os.environ.get("PORT", 8080))
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

analyzer = SafetyAnalyzer()

class AppRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/taxonomies":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = {
                "allergens": [
                    {"id": k, "label": v["label"], "severity": v["severity_default"]}
                    for k, v in ALLERGEN_TAXONOMY.items()
                ],
                "diets": [
                    {"id": k, "label": v["label"]}
                    for k, v in DIETARY_RULES.items()
                ]
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif parsed.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "allergy-diet-guard"}).encode("utf-8"))
        else:
            # Serve index.html or static assets
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/analyze":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                payload = json.loads(body)
                ingredients = payload.get("ingredients", "")
                profile = payload.get("profile", {})
                result = analyzer.analyze(ingredients, profile)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), AppRequestHandler) as httpd:
        print(f"==================================================")
        print(f"[*] Allergy & Diet Guard (SafeBite AI) Server")
        print(f"[>] Local UI: http://localhost:{PORT}")
        print(f"[>] Open Source AI inference: Ready (Offline + Ollama)")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
