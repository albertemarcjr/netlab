# data/

Everything in here except this README is gitignored. Data is large, it may be sensitive, and it can always be regenerated from code.

- **`raw/`** holds inputs, either downloaded or generated. Never edit these by hand. If one is wrong, fix the code that produces it and regenerate.
- **`processed/`** holds derived outputs (SQLite files, Parquet exports, received records). It is safe to delete at any time and can always be rebuilt from `raw/` plus code.

Paths to these folders come from `src/netlab/paths.py` (`paths.DATA_RAW`, `paths.DATA_PROCESSED`), never from strings typed in code.

## What goes here, and how to regenerate it

| File | Made by | How to regenerate |
|---|---|---|
| `raw/orders.csv`, `raw/orders.log` | notebook 02 §C (mock shop orders, seeded) | re-run notebook 02 §C |
| `raw/country-codes.csv` + `.provenance.json` | notebook 02 §C, downloaded from GitHub (datasets/country-codes) | delete it and re-run the download cell |
| `raw/orders_small.csv` | `scripts/make_orders.py` (02 §E) | `uv run python scripts/make_orders.py --rows 1000 --seed 7 --out data/raw/orders_small.csv` |
| `raw/orders_big.parquet` | `make-orders` (02 §G) | see the command in notebook 02 §G |
| `processed/netlab.sqlite` | notebook 03 §F | re-run notebook 03 §F |
| `processed/received_orders.jsonl` | the inventory API's `POST /orders` (03 §C) | post the orders again |
| `processed/products.parquet` | `scripts/collect.py` (03 §I) | run the script |

## Downloaded sources

- Country codes (ISO 3166), from the Open Knowledge Foundation's datasets project:
  `https://raw.githubusercontent.com/datasets/country-codes/main/data/country-codes.csv`
  (checked reachable on 2026-11-17). Each download writes a provenance file next to the data with the URL, retrieval time, byte count and SHA-256.
