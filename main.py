"""
Hacktoberfest 2026 — Unified Monorepo Gateway
Single Web Service router for Render free tier.
Routes:
  /          -> Challenge Suite Portal Dashboard
  /weekend/  -> 00-weekend-allergy-guard (Allergy & Diet Guard App)
  /week-1/   -> Week 1 App (Oct 5)
  /week-2/   -> Week 2 App (Oct 12)
  /week-3/   -> Week 3 App (Oct 19)
  /week-4/   -> Week 4 App (Oct 26)
"""

import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", 8080))

# Import analyzer from 00-weekend-allergy-guard
WEEKEND_DIR = os.path.join(BASE_DIR, "00-weekend-allergy-guard")
sys.path.insert(0, WEEKEND_DIR)
try:
    from analyzer import SafetyAnalyzer, ALLERGEN_TAXONOMY, DIETARY_RULES
    weekend_analyzer = SafetyAnalyzer()
except ImportError:
    weekend_analyzer = None
    ALLERGEN_TAXONOMY, DIETARY_RULES = {}, {}

# Import engine from 01-week-1
WEEK1_DIR = os.path.join(BASE_DIR, "01-week-1")
sys.path.insert(0, WEEK1_DIR)
try:
    from engine import TrailFloraEngine
    week1_engine = TrailFloraEngine()
except ImportError:
    week1_engine = None

# Import engine from 02-week-2
WEEK2_DIR = os.path.join(BASE_DIR, "02-week-2")
sys.path.insert(0, WEEK2_DIR)
try:
    from hustle_engine import HustleLedgerEngine
    week2_engine = HustleLedgerEngine()
except ImportError:
    week2_engine = None

# Import engine from 03-week-3
WEEK3_DIR = os.path.join(BASE_DIR, "03-week-3")
sys.path.insert(0, WEEK3_DIR)
try:
    from sloth_engine import SlothDigestEngine
    week3_engine = SlothDigestEngine()
except ImportError:
    week3_engine = None

class UnifiedHubHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. Health checks
        if path in ("/health", "/api/health"):
            self._send_json({"status": "healthy", "service": "hacktoberfest-2026-hub"})
            return

        # 2. Portal Root Dashboard
        if path in ("/", "/index.html"):
            portal_path = os.path.join(BASE_DIR, "portal.html")
            self._send_html_file(portal_path)
            return

        # 3. Redirect /weekend to /weekend/ and /week-1 to /week-1/
        if path == "/weekend":
            self.send_response(301)
            self.send_header("Location", "/weekend/")
            self.end_headers()
            return

        if path == "/week-1":
            self.send_response(301)
            self.send_header("Location", "/week-1/")
            self.end_headers()
            return

        if path == "/week-2":
            self.send_response(301)
            self.send_header("Location", "/week-2/")
            self.end_headers()
            return

        if path == "/week-3":
            self.send_response(301)
            self.send_header("Location", "/week-3/")
            self.end_headers()
            return

        # 4. Weekend App API routes
        if path == "/weekend/api/taxonomies":
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
            self._send_json(data)
            return

        if path == "/weekend/api/health":
            self._send_json({"status": "healthy", "service": "allergy-diet-guard"})
            return

        # 5. Weekend App Static Files
        if path.startswith("/weekend/"):
            rel_file = path[len("/weekend/"):]
            if not rel_file or rel_file == "index.html":
                file_path = os.path.join(WEEKEND_DIR, "static", "index.html")
            else:
                file_path = os.path.join(WEEKEND_DIR, "static", rel_file)

            if os.path.exists(file_path) and os.path.isfile(file_path):
                self._serve_file(file_path)
                return

        # 6. Week 1 App Static & Health
        if path == "/week-1/api/health":
            self._send_json({"status": "healthy", "service": "trail-flora-ai"})
            return

        if path.startswith("/week-1/"):
            rel_file = path[len("/week-1/"):]
            if not rel_file or rel_file == "index.html":
                file_path = os.path.join(WEEK1_DIR, "static", "index.html")
            else:
                file_path = os.path.join(WEEK1_DIR, "static", rel_file)

            if os.path.exists(file_path) and os.path.isfile(file_path):
                self._serve_file(file_path)
                return

        # 7. Week 2 App Static & Health
        if path == "/week-2/api/health":
            self._send_json({"status": "healthy", "service": "hustle-ledger-ai"})
            return

        if path.startswith("/week-2/"):
            rel_file = path[len("/week-2/"):]
            if not rel_file or rel_file == "index.html":
                file_path = os.path.join(WEEK2_DIR, "static", "index.html")
            else:
                file_path = os.path.join(WEEK2_DIR, "static", rel_file)

            if os.path.exists(file_path) and os.path.isfile(file_path):
                self._serve_file(file_path)
                return

        # 8. Week 3 App Static & Health
        if path == "/week-3/api/health":
            self._send_json({"status": "healthy", "service": "sloth-digest-ai"})
            return

        if path.startswith("/week-3/"):
            rel_file = path[len("/week-3/"):]
            if not rel_file or rel_file == "index.html":
                file_path = os.path.join(WEEK3_DIR, "static", "index.html")
            else:
                file_path = os.path.join(WEEK3_DIR, "static", rel_file)

            if os.path.exists(file_path) and os.path.isfile(file_path):
                self._serve_file(file_path)
                return

        # 9. Upcoming challenges placeholder
        for w in ("week-4",):
            if path.startswith(f"/{w}"):
                self._send_json({
                    "challenge": w,
                    "status": "upcoming",
                    "message": f"This challenge workspace will unlock according to the official Hacktoberfest schedule."
                })
                return

        # 404
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"404 Not Found - Hacktoberfest 2026 AI Suite")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/weekend/api/analyze":
            if not weekend_analyzer:
                self.send_response(500)
                self.end_headers()
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                payload = json.loads(body)
                ingredients = payload.get("ingredients", "")
                profile = payload.get("profile", {})
                result = weekend_analyzer.analyze(ingredients, profile)
                self._send_json(result)
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        # Week 1 App API routes
        if path.startswith("/week-1/api/"):
            if not week1_engine:
                self.send_response(500)
                self.end_headers()
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            if path == "/week-1/api/plant/scan":
                res = week1_engine.identify_plant(payload.get("query", ""))
                self._send_json(res)
                return

            if path == "/week-1/api/garden/plan":
                zone = payload.get("zone", "zone_5_6")
                temp_c = payload.get("temp_c", 10)
                res = week1_engine.plan_garden(zone, temp_c)
                self._send_json(res)
                return

            if path == "/week-1/api/grass/scout":
                temp_c = payload.get("temp_c", 18)
                cloud_pct = payload.get("cloud_pct", 20)
                duration = payload.get("duration_mins", 45)
                res = week1_engine.scout_outdoor_window(cloud_pct, temp_c, duration)
                self._send_json(res)
                return

        # Week 2 App API routes
        if path.startswith("/week-2/api/"):
            if not week2_engine:
                self.send_response(500)
                self.end_headers()
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            if path == "/week-2/api/expense/categorize":
                desc = payload.get("description", "")
                amt = float(payload.get("amount", 0.0))
                res = week2_engine.categorize_expense(desc, amt)
                self._send_json(res)
                return

            if path == "/week-2/api/invoice/generate":
                client = payload.get("client", "")
                project = payload.get("project", "")
                items = payload.get("items", [])
                res = week2_engine.generate_invoice(client, project, items)
                self._send_json(res)
                return

            if path == "/week-2/api/comms/draft":
                comm_type = payload.get("comm_type", "overdue_reminder")
                client = payload.get("client_name", "")
                amt = float(payload.get("amount", 0.0))
                ctx = payload.get("context", "")
                draft = week2_engine.draft_client_communication(comm_type, client, amt, ctx)
                self._send_json({"draft": draft})
                return

        # Week 3 App API routes
        if path.startswith("/week-3/api/"):
            if not week3_engine:
                self.send_response(500)
                self.end_headers()
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            if path == "/week-3/api/triage/distill":
                text = payload.get("text", "")
                alias = payload.get("user_alias", "me")
                res = week3_engine.distill_thread(text, alias)
                self._send_json(res)
                return

            if path == "/week-3/api/winddown/plan":
                ftype = payload.get("fatigue_type", "screen_eye_strain")
                mins = payload.get("minutes", 20)
                res = week3_engine.generate_wind_down(mins, ftype)
                self._send_json(res)
                return

            if path == "/week-3/api/task/simplify":
                task = payload.get("task", "")
                res = week3_engine.simplify_task(task)
                self._send_json(res)
                return

        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _send_html_file(self, path):
        if not os.path.exists(path):
            self.send_response(404)
            self.end_headers()
            return
        with open(path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _serve_file(self, path):
        content_type = "application/octet-stream"
        if path.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        elif path.endswith(".css"):
            content_type = "text/css"
        elif path.endswith(".js"):
            content_type = "application/javascript"
        elif path.endswith(".png"):
            content_type = "image/png"
        elif path.endswith(".svg"):
            content_type = "image/svg+xml"

        with open(path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), UnifiedHubHandler) as httpd:
        print(f"==================================================")
        print(f"[*] Hacktoberfest 2026 Unified Hub Gateway")
        print(f"[>] Portal:  http://localhost:{PORT}/")
        print(f"[>] Weekend: http://localhost:{PORT}/weekend/")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()
