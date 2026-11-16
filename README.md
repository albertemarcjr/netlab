# netlab

A learning workspace for writing code, taught through networking and security. It contains three notebooks you work through in order, a small Python package that grows as you write it, scripts, two local services, and a Postgres setup.

The exercises are yours to solve. Any AI assistant working in this repo is told to coach you instead of solving them (see `AGENTS.md`). When you're genuinely stuck, say "show me the code".

## Setup (once)

You need [uv](https://docs.astral.sh/uv/) and git. Docker is optional (only notebook 03 §F uses it).

```bash
cd ~/code/netlab
uv sync                      # creates .venv/ from uv.lock: the exact same packages, every time
cp .env.example .env         # then put real values in .env (it is gitignored)
```

## The order

1. `notebooks/01_shapes_and_walking_them.ipynb`: data shapes, and the logic that walks them
2. `notebooks/02_libraries_modules_scripts.ipynb`: where code comes from, modules, scripts, cores, pandas vs polars
3. `notebooks/03_clients_servers_and_data.ipynb`: sockets, HTTP, APIs, failure, databases, data formats. Needs extra terminals for the services.

Start the notebooks with:

```bash
uv run jupyter lab
```

Or open this folder in VS Code or Cursor and pick the `.venv` kernel.

## How to run

| What | Command (from the repo root) |
|---|---|
| Notebooks | `uv run jupyter lab` |
| Tests | `uv run pytest` |
| Echo server (03 §A) | `uv run python services/echo_server.py` |
| Inventory API (03 §C) | `uv run python services/inventory_api.py` |
| Postgres (03 §F) | `docker compose -f services/docker-compose.yml --env-file .env up -d` |

You will add rows to this table as you build things (notebook 02 §E, notebook 03 §I).

## How the repo is organized

- **One folder, one job.** `src/netlab/` is code you import. `scripts/` is code you run. `services/` is things that stay running. `notebooks/` is exploration. `data/` is never code. `tests/` checks `src/`.
- **Data is never committed.** It is large, it may be sensitive, and it can be regenerated. The repo holds the code that produces the data, and `data/README.md` says how.
- **Dependencies are declared and locked, and the installed packages are never committed.** `pyproject.toml` says what you need. `uv.lock` records exactly what you got. `.venv/` is a disposable build product.
- **Secrets never enter the repo.** `.env` holds real values and is gitignored. `.env.example` documents the variable names.
- **Entry points are obvious.** This file gives the one setup command and one command for each thing you can run. Each folder that isn't self-explanatory has its own short README.
- **Paths are defined once**, in `src/netlab/paths.py`, never typed as strings scattered through the code.

```
netlab/
├── README.md          this file
├── AGENTS.md          rules for AI assistants (CLAUDE.md points here)
├── pyproject.toml     project metadata, dependencies, entry points
├── uv.lock            exact resolved versions (committed)
├── .env.example       names of the environment variables, with fake values
├── notebooks/         01 → 02 → 03
├── src/netlab/        the importable package; you add modules to it
├── scripts/           thin entry points that import from src/
├── services/          echo server, inventory API, Postgres (see services/README.md)
├── tests/             pytest tests for src/
└── data/              gitignored except its README (raw/ and processed/)
```

`docs/curriculum.md` (the design of this course) is kept on your machine only and is gitignored.
