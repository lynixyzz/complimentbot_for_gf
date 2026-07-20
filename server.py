"""Мини-сервер для Telegram WebApp: отдаёт страницу со сферой и /phrase (фразу дня)."""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from config import BASE_DIR, WEBAPP_PORT
from content import phrase_of_day

INDEX = (BASE_DIR / "webapp" / "index.html").read_bytes()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/phrase"):
            body = json.dumps({"phrase": phrase_of_day()}, ensure_ascii=False).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
        elif self.path in ("/", "/index.html"):
            self._send(200, INDEX, "text/html; charset=utf-8")
        else:
            self._send(404, b"not found", "text/plain")

    def log_message(self, *_):  # тихо
        pass


def start() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", WEBAPP_PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True, name="webapp").start()
