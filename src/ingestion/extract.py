"""CSV extraction for the immutable MarketMosaic source dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    from validation import EXPECTED_COLUMNS
except ModuleNotFoundError:
    from src.validation import EXPECTED_COLUMNS


class ExtractionError(ValueError):
    """Raised when the source file cannot be safely extracted."""


def extract_csv(file_path: str | Path) -> pd.DataFrame:
    """Read a source CSV without changing its raw columns or values."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Source CSV does not exist: {path}")
    try:
        data = pd.read_csv(path)
    except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
        raise ExtractionError(f"Unable to read source CSV {path}: {exc}") from exc
    missing = sorted(set(EXPECTED_COLUMNS) - set(data.columns))
    if missing:
        raise ExtractionError(f"Source CSV is missing required columns: {missing}")
    if data.empty:
        raise ExtractionError(f"Source CSV contains no rows: {path}")
    data = data.copy()
    data["time_dt"] = pd.to_datetime(data["time"], errors="coerce")
    if data["time_dt"].isna().any():
        raise ExtractionError("Source CSV contains unparseable values in 'time'.")
    return data
