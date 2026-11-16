"""The single place that defines where things live in this repo."""

from pathlib import Path

# Paths come from this file's location, not the current working directory.
# A notebook's working directory is notebooks/; a script's is wherever you ran it
# from. __file__ is always src/netlab/paths.py, so ROOT is the same for both.
ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
DATA_PROCESSED = DATA / "processed"


def ensure_dirs() -> None:
    """Create the data folders if they don't exist yet (safe to call repeatedly)."""
    for d in (DATA_RAW, DATA_PROCESSED):
        d.mkdir(parents=True, exist_ok=True)
