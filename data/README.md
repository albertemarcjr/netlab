# data/

Everything in here except this README is gitignored. Data is large, it may be sensitive, and it can always be regenerated from code.

- **`raw/`** holds inputs, either downloaded or generated. Never edit these by hand. If one is wrong, fix the code that produces it and regenerate.
- **`processed/`** holds derived outputs (SQLite files, Parquet exports, received records). It is safe to delete at any time and can always be rebuilt from `raw/` plus code.

Paths to these folders come from `src/netlab/paths.py` (`paths.DATA_RAW`, `paths.DATA_PROCESSED`), never from strings typed in code.

## What goes here, and how to regenerate it

| File | Made by | How to regenerate |
|---|---|---|
| `raw/flows.csv`, `raw/flows.log` | notebook 02 §C (mock flows, seeded) | re-run notebook 02 §C |
| `raw/service-names-port-numbers.csv` + `.provenance.json` | notebook 02 §C, downloaded from IANA | delete it and re-run the download cell |
| `raw/flows_small.csv` | `scripts/make_flows.py` (02 §E) | `uv run python scripts/make_flows.py --rows 1000 --seed 7 --out data/raw/flows_small.csv` |
| `raw/flows_big.parquet` | `make-flows` (02 §G) | see the command in notebook 02 §G |
| `processed/netlab.sqlite` | notebook 03 §F | re-run notebook 03 §F |
| `processed/received_flows.jsonl` | the inventory API's `POST /flows` (03 §C) | post the flows again |
| `processed/devices.parquet` | `scripts/collect.py` (03 §I) | run the script |

## Downloaded sources

- IANA Service Name and Transport Protocol Port Number Registry:
  `https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv`
  (reachable when this repo was built on 2026-11-16, so no substitute source was needed). Each download writes a provenance file next to the data with the URL, retrieval time, byte count and SHA-256.
