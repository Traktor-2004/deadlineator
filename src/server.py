"""Small loopback-only HTTP server for the Deadlineator demo."""

from __future__ import annotations

import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from deadlineator import add_task, change_status, list_tasks


ROOT = Path(__file__).resolve().parent
DATA_FILE = Path(
    os.environ.get("DEADLINEATOR_DATA", str(ROOT.parent / "data" / "tasks.json"))
)
STATIC_FILES = {
    "/": (ROOT / "static" / "index.html", "text/html; charset=utf-8"),
    "/app.js": (ROOT / "static" / "app.js", "text/javascript; charset=utf-8"),
    "/styles.css": (ROOT / "static" / "styles.css", "text/css; charset=utf-8"),
}


class DeadlineatorHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, value: object) -> None:
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def _read_json(self) -> dict[str, object]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("invalid Content-Length") from exc
        if length < 1 or length > 16_384:
            raise ValueError("request body must be between 1 and 16384 bytes")
        try:
            value = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("request body must be valid UTF-8 JSON") from exc
        if not isinstance(value, dict):
            raise ValueError("request body must be a JSON object")
        return value

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        path = urlsplit(self.path).path
        if path == "/api/tasks":
            self._send_json(200, list_tasks(DATA_FILE))
            return
        static = STATIC_FILES.get(path)
        if static is None:
            self._send_json(404, {"error": "not found"})
            return
        file_path, content_type = static
        self._send(200, file_path.read_bytes(), content_type)

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if urlsplit(self.path).path != "/api/tasks":
            self._send_json(404, {"error": "not found"})
            return
        try:
            values = self._read_json()
            task = add_task(
                DATA_FILE,
                title=values.get("title"),
                due_date=values.get("due_date"),
                priority=values.get("priority", "medium"),
                team=values.get("team", "Core"),
                description=values.get("description", ""),
            )
        except (ValueError, TypeError) as exc:
            self._send_json(400, {"error": str(exc)})
            return
        self._send_json(201, task)

    def do_PATCH(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        match = re.fullmatch(r"/api/tasks/([A-Za-z0-9_-]{1,64})", urlsplit(self.path).path)
        if match is None:
            self._send_json(404, {"error": "not found"})
            return
        try:
            values = self._read_json()
            task = change_status(DATA_FILE, match.group(1), str(values.get("status", "")))
        except KeyError:
            self._send_json(404, {"error": "task not found"})
            return
        except (ValueError, TypeError) as exc:
            self._send_json(400, {"error": str(exc)})
            return
        self._send_json(200, task)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), DeadlineatorHandler)
    print("Дедлайнатор запущен: http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
