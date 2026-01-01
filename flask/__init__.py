"""
A tiny, dependency-free stand-in for Flask used in this offline environment.
It implements just enough of the API used by the practice project:
- Flask class with route registration and a minimal test client
- jsonify helper
- request object that carries parsed JSON

This is **not** a drop-in replacement for the real Flask package but keeps
the learning experience intact when package installation is blocked.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Callable, Dict, List, Tuple


class _Request:
    def __init__(self) -> None:
        self._json: Any = None

    def set_json(self, value: Any) -> None:
        self._json = value

    def get_json(self, silent: bool = False) -> Any:
        if self._json is None and not silent:
            raise ValueError("No JSON payload available")
        return self._json


request = _Request()


def jsonify(obj: Any) -> Any:
    """Return the object as-is; the test client will wrap it in a response."""
    return obj


class _TestResponse:
    def __init__(self, data: Any, status_code: int) -> None:
        self._data = data
        self.status_code = status_code

    def get_json(self) -> Any:
        return self._data


class _TestClient:
    def __init__(self, app: "Flask") -> None:
        self.app = app

    def __enter__(self) -> "_TestClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        return None

    def _invoke(self, method: str, path: str, payload: Any = None) -> _TestResponse:
        request.set_json(payload)
        handler = self.app.routes.get((method, path))
        if handler is None:
            return _TestResponse({"error": "Not found"}, 404)

        result = handler()

        if isinstance(result, tuple):
            body, status = result
        else:
            body, status = result, 200

        return _TestResponse(body, status)

    def get(self, path: str, **_: Any) -> _TestResponse:
        return self._invoke("GET", path)

    def post(self, path: str, data: Any = None, **_: Any) -> _TestResponse:
        payload = None
        if data is not None:
            payload = json.loads(data)
        return self._invoke("POST", path, payload)


class Flask:
    def __init__(self, name: str) -> None:
        self.name = name
        self.routes: Dict[Tuple[str, str], Callable[[], Any]] = {}

    def route(self, path: str, methods: List[str]):
        def decorator(func: Callable[[], Any]):
            for method in methods:
                self.routes[(method.upper(), path)] = func
            return func

        return decorator

    def get(self, path: str):
        return self.route(path, ["GET"])

    def post(self, path: str):
        return self.route(path, ["POST"])

    def test_client(self) -> _TestClient:
        return _TestClient(self)

    def run(self, host: str = "127.0.0.1", port: int = 5000, debug: bool = False) -> None:
        app = self

        class Handler(BaseHTTPRequestHandler):
            def _send_json(self, body: Any, status: int) -> None:
                encoded = json.dumps(body).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def do_GET(self):  # type: ignore
                handler = app.routes.get(("GET", self.path))
                if handler is None:
                    self._send_json({"error": "Not found"}, 404)
                    return
                request.set_json(None)
                result = handler()
                if isinstance(result, tuple):
                    body, status = result
                else:
                    body, status = result, 200
                self._send_json(body, status)

            def do_POST(self):  # type: ignore
                content_length = int(self.headers.get("Content-Length", 0))
                payload = None
                if content_length:
                    raw = self.rfile.read(content_length)
                    try:
                        payload = json.loads(raw)
                    except json.JSONDecodeError:
                        payload = None
                request.set_json(payload)
                handler = app.routes.get(("POST", self.path))
                if handler is None:
                    self._send_json({"error": "Not found"}, 404)
                    return
                result = handler()
                if isinstance(result, tuple):
                    body, status = result
                else:
                    body, status = result, 200
                self._send_json(body, status)

        server = HTTPServer((host, port), Handler)
        if debug:
            print(f"* Running development server at http://{host}:{port}")
        server.serve_forever()
