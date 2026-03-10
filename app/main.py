from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict[str, str]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/":
            self._send_json(HTTPStatus.OK, {"message": "DEMPA ERP S STEM API is running"})
            return
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})


def create_server(host: str = "0.0.0.0", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), RequestHandler)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = create_server(host, port)
    print(f"Server running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
