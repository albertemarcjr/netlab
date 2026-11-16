# services/

Long-running processes. Each one blocks forever waiting for connections, so each runs in **its own terminal**, not in a notebook cell. Run every command from the repo root. Stop a service with Ctrl+C.

| Service | Start | Listens on | Used in |
|---|---|---|---|
| Echo server: raw TCP, sends back what it receives | `uv run python services/echo_server.py` | `127.0.0.1:9000` (`--host`, `--port` to change) | 03 §A |
| Inventory API: HTTP JSON, stdlib `http.server` | `uv run python services/inventory_api.py` | `127.0.0.1:8000` (`--host`, `--port` to change) | 03 §C, §E, §H, §I |
| Postgres 17 in Docker | `docker compose -f services/docker-compose.yml --env-file .env up -d` | `127.0.0.1:5432` (`POSTGRES_PORT` in `.env`) | 03 §F |

Postgres commands:

```bash
docker compose -f services/docker-compose.yml --env-file .env ps        # is it running?
docker compose -f services/docker-compose.yml --env-file .env down      # stop; data kept in the volume
docker compose -f services/docker-compose.yml --env-file .env down -v   # stop and delete the data
```

Check what's listening on a port: `lsof -nP -iTCP:8000 -sTCP:LISTEN`.

Both Python services bind to `127.0.0.1` by default, which makes them reachable from this machine only. `--host 0.0.0.0` exposes them on every network interface. Notebook 03 §A shows the difference.

`inventory_api.py` has two `TODO (learner)` handlers for you to write in notebook 03 §C: `GET /devices/<name>` and `POST /flows`.
