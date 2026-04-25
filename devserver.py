import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8000
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_FILE = BASE_DIR / "techstackpage.html"


def load_content():
    namespace = {}
    content_file = BASE_DIR / "content.py"
    exec(content_file.read_text(encoding="utf-8"), namespace)
    return namespace.get("CONTENT", [])


class TechStackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/techstackpage.html"):
            self.serve_template()
            return

        if self.path == "/content-data":
            self.serve_content_data()
            return

        self.send_error(404, "Not Found")

    def serve_template(self):
        html = TEMPLATE_FILE.read_text(encoding="utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def serve_content_data(self):
        data = json.dumps(load_content(), ensure_ascii=False, indent=2)
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), TechStackHandler)
    print(f"Serving http://{HOST}:{PORT}")
    server.serve_forever()
