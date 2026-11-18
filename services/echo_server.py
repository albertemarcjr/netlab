"""An echo server: whatever bytes a client sends, it sends straight back.

Run (from the repo root, in its own terminal):
    uv run python services/echo_server.py                  # 127.0.0.1:9000, this machine only
    uv run python services/echo_server.py --host 0.0.0.0   # every interface (notebook 03 §A)
Stop: Ctrl+C
"""

import argparse
import socket


def serve(host: str, port: int) -> None:
    # A socket is one endpoint of a connection. AF_INET = IPv4, SOCK_STREAM = TCP.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        # Let a restarted server take the port again at once instead of waiting out TIME_WAIT.
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((host, port))  # claim address:port; fails if another process holds it
        listener.listen()  # the kernel now completes handshakes and queues new connections
        print(f"echo server listening on {host}:{port}", flush=True)
        while True:
            conn, addr = listener.accept()  # blocks until a client connects; one at a time
            with conn:  # closes the client's connection when this block ends
                print(f"client connected from {addr[0]}:{addr[1]}", flush=True)
                while True:
                    data = conn.recv(4096)  # up to 4096 bytes; b"" means the client closed
                    if not data:
                        break
                    # TODO (learner), notebook 03 §A Exercise 1: reply with the message
                    # uppercased, a space, then the server's current time in ISO format.
                    conn.sendall(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Raw TCP echo server.")
    parser.add_argument("--host", default="127.0.0.1", help="bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9000, help="TCP port (default: 9000)")
    args = parser.parse_args()
    try:
        serve(args.host, args.port)
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
