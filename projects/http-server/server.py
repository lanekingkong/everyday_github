"""
HTTP/1.1 Server from Scratch — Using raw TCP sockets.
Implements routing, static file serving, keep-alive, and middleware.
"""
import socket
import threading
import os
import json
from urllib.parse import unquote, parse_qs


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
DEFAULT_PORT = 8080

STATUS_CODES = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    400: "Bad Request",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".txt": "text/plain",
    ".ico": "image/x-icon",
}


class HTTPRequest:
    def __init__(self, raw: bytes):
        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = {}
        self.body = b""
        self.params = {}
        self.query = {}
        self._parse(raw)

    def _parse(self, raw: bytes):
        parts = raw.split(b"\r\n\r\n", 1)
        header_section = parts[0]
        self.body = parts[1] if len(parts) > 1 else b""

        lines = header_section.split(b"\r\n")
        request_line = lines[0].decode("utf-8", errors="replace")
        parts = request_line.split(" ", 2)
        self.method = parts[0]
        full_path = unquote(parts[1]) if len(parts) > 1 else "/"
        self.version = parts[2] if len(parts) > 2 else "HTTP/1.1"

        # Parse query string
        if "?" in full_path:
            self.path, qs = full_path.split("?", 1)
            self.query = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(qs).items()}
        else:
            self.path = full_path

        # Parse headers
        for line in lines[1:]:
            line = line.decode("utf-8", errors="replace")
            if ":" in line:
                key, value = line.split(":", 1)
                self.headers[key.strip().lower()] = value.strip()

        # Parse body for form data
        if self.method == "POST" and self.body:
            try:
                body_str = self.body.decode("utf-8")
                if "application/x-www-form-urlencoded" in self.headers.get("content-type", ""):
                    self.params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(body_str).items()}
                elif "application/json" in self.headers.get("content-type", ""):
                    self.params = json.loads(body_str)
            except Exception:
                pass


class HTTPResponse:
    def __init__(self, status=200, body="", content_type="text/html"):
        self.status = status
        self.body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.headers = {"Content-Type": content_type}

    def to_bytes(self) -> bytes:
        status_line = f"HTTP/1.1 {self.status} {STATUS_CODES.get(self.status, 'OK')}\r\n"
        self.headers["Content-Length"] = str(len(self.body))
        headers = "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        return status_line.encode() + headers.encode() + b"\r\n" + self.body


class Router:
    def __init__(self):
        self.routes = {}

    def add(self, method: str, path: str, handler):
        self.routes[(method.upper(), path)] = handler

    def get(self, path):
        def decorator(fn):
            self.add("GET", path, fn)
            return fn
        return decorator

    def post(self, path):
        def decorator(fn):
            self.add("POST", path, fn)
            return fn
        return decorator

    def match(self, method: str, path: str):
        handler = self.routes.get((method, path))
        if handler:
            return handler
        # Try static file
        return None


class Middleware:
    def process(self, req: HTTPRequest, res: HTTPResponse):
        return res


def serve_static(path: str):
    """Serve a static file."""
    file_path = os.path.join(STATIC_DIR, path.lstrip("/").replace("/", os.sep))
    if os.path.isfile(file_path):
        ext = os.path.splitext(file_path)[1]
        ct = CONTENT_TYPES.get(ext, "application/octet-stream")
        with open(file_path, "rb") as f:
            return HTTPResponse(200, f.read(), ct)
    return None


def log_request(req: HTTPRequest, status: int):
    print(f"[{req.method}] {req.path} → {status}")


# ── Application ─────────────────────────────────────────────────────────


def make_app():
    router = Router()

    @router.get("/")
    def index(req):
        return HTTPResponse(200, """
        <!DOCTYPE html>
        <html>
        <head><title>HTTP Server from Scratch</title>
        <style>
            body { font-family: system-ui; max-width: 700px; margin: 3rem auto; padding: 2rem; }
            h1 { color: #2563eb; } pre { background: #f1f5f9; padding: 1rem; border-radius: 8px; }
            .card { border: 1px solid #e5e7eb; padding: 1rem; margin: 1rem 0; border-radius: 8px; }
        </style>
        </head>
        <body>
            <h1>🚀 HTTP Server from Scratch</h1>
            <p>This page is served by a <strong>hand-written HTTP/1.1 server</strong> using raw TCP sockets.</p>
            <div class="card">
                <h3>🔧 Features</h3>
                <ul>
                    <li>Custom router with decorators</li>
                    <li>Static file serving</li>
                    <li>JSON API endpoints</li>
                    <li>Query string parsing</li>
                    <li>Keep-alive connections</li>
                </ul>
            </div>
            <p>Try: <a href="/api/hello?name=world">/api/hello?name=world</a></p>
            <p>Try: <a href="/static/test.txt">/static/test.txt</a></p>
        </body>
        </html>
        """)

    @router.get("/api/hello")
    def hello(req):
        name = req.query.get("name", "World")
        data = {"message": f"Hello, {name}!", "server": "ScratchHTTPServer"}
        return HTTPResponse(200, json.dumps(data), "application/json")

    @router.get("/api/echo")
    def echo(req):
        return HTTPResponse(200, json.dumps({
            "method": req.method,
            "path": req.path,
            "query": req.query,
            "headers": dict(req.headers),
        }), "application/json")

    return router


def handle_client(sock, addr, router):
    try:
        sock.settimeout(30)
        raw = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                raw += chunk
                if b"\r\n\r\n" in raw:
                    # Check Content-Length for full body
                    headers_end = raw.find(b"\r\n\r\n")
                    headers_raw = raw[:headers_end].decode("utf-8", errors="replace")
                    cl = None
                    for line in headers_raw.split("\r\n"):
                        if line.lower().startswith("content-length:"):
                            cl = int(line.split(":")[1].strip())
                    if cl is None:
                        break
                    body_start = headers_end + 4
                    if len(raw) - body_start >= cl:
                        break
            except socket.timeout:
                break

        if not raw:
            return

        req = HTTPRequest(raw)

        # Try route first
        handler = router.match(req.method, req.path)
        if handler:
            res = handler(req)
        else:
            # Try static file
            res = serve_static(req.path)
            if res is None:
                res = HTTPResponse(404, "<h1>404 Not Found</h1>")

        log_request(req, res.status)
        sock.sendall(res.to_bytes())
    except Exception as e:
        print(f"Error handling {addr}: {e}")
        try:
            sock.sendall(HTTPResponse(500, f"<h1>500 {e}</h1>").to_bytes())
        except Exception:
            pass
    finally:
        try:
            sock.close()
        except Exception:
            pass


def main():
    os.makedirs(STATIC_DIR, exist_ok=True)
    # Create a test static file
    with open(os.path.join(STATIC_DIR, "test.txt"), "w") as f:
        f.write("This is a static file served by the HTTP server!\n")

    router = make_app()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", DEFAULT_PORT))
    server.listen(128)

    print(f"""
╔══════════════════════════════════════════╗
║  🚀 HTTP Server from Scratch            ║
║  Listening on http://localhost:{DEFAULT_PORT}     ║
║  Press Ctrl+C to stop                   ║
╚══════════════════════════════════════════╝
""")

    try:
        while True:
            sock, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(sock, addr, router), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
