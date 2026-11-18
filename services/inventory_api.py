"""Inventory API: a small shop's product catalog, served as JSON over HTTP. Standard library only.

Run (from the repo root, in its own terminal):
    uv run python services/inventory_api.py      # http://127.0.0.1:8000
Stop: Ctrl+C

Endpoints
    GET  /health            {"status": "ok"}
    GET  /products          every product, as a list of JSON objects
    GET  /products/<name>   one product; 404 if unknown             TODO (learner)
    POST /orders            store one JSON order                    TODO (learner)
    GET  /slow?seconds=N    waits N seconds, then answers (timeouts, notebook 03 §E, §H)
    GET  /boom              always 500: a bug on the server side
    GET  /flaky             fails the first 2 of every 3 calls with 503 (retries, §E)
"""

import argparse
import json
import threading
import time
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from netlab import paths


@dataclass
class Product:  # like the Product dataclass in notebook 01 §E
    name: str
    price_cents: int
    stock: int
    category: str


# A small shop's catalog: name -> (price in cents, how many in stock, category)
_CATALOG = {
    "apple": (50, 120, "fruit"),
    "bread": (325, 40, "bakery"),
    "milk": (199, 60, "dairy"),
    "coffee": (875, 25, "drinks"),
    "cheese": (640, 30, "dairy"),
    "eggs": (420, 50, "dairy"),
    "tea": (350, 45, "drinks"),
    "honey": (760, 15, "pantry"),
    "jam": (450, 20, "pantry"),
}
PRODUCTS = {name: Product(name, price, stock, category) for name, (price, stock, category) in _CATALOG.items()}

RECEIVED_ORDERS = paths.DATA_PROCESSED / "received_orders.jsonl"

_flaky_lock = threading.Lock()  # requests arrive on several threads; guard the shared counter
_flaky_calls = 0


class Handler(BaseHTTPRequestHandler):
    # HTTP/1.1 keeps the connection open between requests (connection reuse, 03 §H).
    # That only works if every response says how long its body is (Content-Length).
    protocol_version = "HTTP/1.1"

    def send_json(self, status: int, body) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        global _flaky_calls
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        if url.path == "/health":
            self.send_json(200, {"status": "ok"})
        elif url.path == "/products":
            self.send_json(200, [asdict(p) for p in PRODUCTS.values()])
        elif len(parts) == 2 and parts[0] == "products":
            self.get_product(parts[1])
        elif url.path == "/slow":
            seconds = float(parse_qs(url.query).get("seconds", ["1"])[0])
            time.sleep(min(seconds, 30))
            self.send_json(200, {"slept": seconds})
        elif url.path == "/boom":
            self.send_json(500, {"error": "something broke on the server"})
        elif url.path == "/flaky":
            with _flaky_lock:
                _flaky_calls += 1
                n = _flaky_calls
            if n % 3 == 0:
                self.send_json(200, {"status": "ok", "call": n})
            else:
                self.send_json(503, {"error": "temporarily unavailable", "call": n})
        else:
            self.send_json(404, {"error": f"no route for {url.path}"})

    def do_POST(self) -> None:
        if urlparse(self.path).path == "/orders":
            self.post_order()
        else:
            self.close_connection = True  # we didn't read the body, so don't reuse this connection
            self.send_json(404, {"error": f"no route for {self.path}"})

    def get_product(self, name: str) -> None:
        """TODO (learner), notebook 03 §C.

        Respond 200 with the product as JSON (asdict, like /products does for each one),
        or 404 with {"error": "no such product"} if name is not a key of PRODUCTS.
        """
        self.send_json(501, {"error": "not implemented yet: GET /products/<name>"})

    def post_order(self) -> None:
        """TODO (learner), notebook 03 §C.

        Read the request body (its size in bytes is in the Content-Length header; read
        exactly that many from self.rfile), parse it as JSON, append it as one line to
        RECEIVED_ORDERS (call paths.ensure_dirs() first), and respond 201 {"status": "stored"}.
        If the body is not valid JSON, respond 400 {"error": "invalid JSON"}.
        """
        self.close_connection = True  # the body is left unread; remove this line once you read it
        self.send_json(501, {"error": "not implemented yet: POST /orders"})

    def log_message(self, fmt, *args) -> None:  # one short line per request, to the terminal
        print(f"{self.client_address[0]} {fmt % args}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory API (stdlib http.server).")
    parser.add_argument("--host", default="127.0.0.1", help="bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="port number (default: 8000)")
    args = parser.parse_args()
    # ThreadingHTTPServer handles each connection on its own thread, so one slow
    # request (/slow) doesn't block everyone else.
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"inventory API on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
