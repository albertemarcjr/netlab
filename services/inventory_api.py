"""Inventory API: the notebook 01 topology, served as JSON over HTTP. Standard library only.

Run (from the repo root, in its own terminal):
    uv run python services/inventory_api.py      # http://127.0.0.1:8000
Stop: Ctrl+C

Endpoints
    GET  /health            {"status": "ok"}
    GET  /devices           every device, as a list of JSON objects
    GET  /devices/<name>    one device; 404 if unknown              TODO (learner)
    POST /flows             store one JSON flow record              TODO (learner)
    GET  /slow?seconds=N    waits N seconds, then answers (timeouts, notebook 03 §E, §H)
    GET  /boom              always 500: a bug on the server side
    GET  /flaky             fails the first 2 of every 3 calls with 503 (retries, §E)
"""

import argparse
import json
import threading
import time
from dataclasses import asdict, dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from netlab import paths


@dataclass
class Device:  # the same dataclass as notebook 01 §E
    name: str
    ip: str
    role: str
    links: list[str] = field(default_factory=list)


# The notebook 01 topology: name -> (ip, role, links)
_TOPOLOGY = {
    "edge-rtr": ("10.255.0.1", "internet-edge", ["fw-01"]),
    "fw-01": ("10.255.0.2", "firewall", ["edge-rtr", "core-rtr-01", "core-rtr-02"]),
    "core-rtr-01": ("10.0.0.1", "core", ["fw-01", "core-rtr-02", "dist-sw-01", "dist-sw-02"]),
    "core-rtr-02": ("10.0.0.2", "core", ["fw-01", "core-rtr-01", "dist-sw-01", "dist-sw-02"]),
    "dist-sw-01": ("10.10.0.1", "distribution", ["core-rtr-01", "core-rtr-02", "acc-sw-01", "acc-sw-02"]),
    "dist-sw-02": ("10.20.0.1", "distribution", ["core-rtr-01", "core-rtr-02", "acc-sw-03"]),
    "acc-sw-01": ("10.10.1.1", "access", ["dist-sw-01"]),
    "acc-sw-02": ("10.10.2.1", "access", ["dist-sw-01"]),
    "acc-sw-03": ("10.20.30.1", "access", ["dist-sw-02"]),
}
DEVICES = {name: Device(name, ip, role, links) for name, (ip, role, links) in _TOPOLOGY.items()}

RECEIVED_FLOWS = paths.DATA_PROCESSED / "received_flows.jsonl"

_flaky_lock = threading.Lock()  # requests arrive on several threads; guard the shared counter
_flaky_calls = 0


class Handler(BaseHTTPRequestHandler):
    # HTTP/1.1 keeps the TCP connection open between requests (connection reuse, 03 §H).
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
        elif url.path == "/devices":
            self.send_json(200, [asdict(d) for d in DEVICES.values()])
        elif len(parts) == 2 and parts[0] == "devices":
            self.get_device(parts[1])
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
        if urlparse(self.path).path == "/flows":
            self.post_flow()
        else:
            self.close_connection = True  # we didn't read the body, so don't reuse this connection
            self.send_json(404, {"error": f"no route for {self.path}"})

    def get_device(self, name: str) -> None:
        """TODO (learner), notebook 03 §C.

        Respond 200 with the device as JSON (asdict, like /devices does for each one),
        or 404 with {"error": "no such device"} if name is not a key of DEVICES.
        """
        self.send_json(501, {"error": "not implemented yet: GET /devices/<name>"})

    def post_flow(self) -> None:
        """TODO (learner), notebook 03 §C.

        Read the request body (its size in bytes is in the Content-Length header; read
        exactly that many from self.rfile), parse it as JSON, append it as one line to
        RECEIVED_FLOWS (call paths.ensure_dirs() first), and respond 201 {"status": "stored"}.
        If the body is not valid JSON, respond 400 {"error": "invalid JSON"}.
        """
        self.close_connection = True  # the body is left unread; remove this line once you read it
        self.send_json(501, {"error": "not implemented yet: POST /flows"})

    def log_message(self, fmt, *args) -> None:  # one short line per request, to the terminal
        print(f"{self.client_address[0]} {fmt % args}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory API (stdlib http.server).")
    parser.add_argument("--host", default="127.0.0.1", help="bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="TCP port (default: 8000)")
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
