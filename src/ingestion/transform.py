"""Deterministic source-to-star-schema transformations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

try:
    from validation import EXPECTED_COLUMNS
except ModuleNotFoundError:
    from src.validation import EXPECTED_COLUMNS

PAID_CHANNELS = [f"Channel{i}" for i in range(5)]
ORGANIC_CHANNEL = "Organic_channel0"


class TransformationError(ValueError):
    """Raised when source data cannot produce valid fact rows."""


@dataclass(frozen=True)
class TransformResult:
    """All dimension and fact frames required by the MySQL schema."""

    staging: pd.DataFrame
    geography: pd.DataFrame
    dates: pd.DataFrame
    channels: pd.DataFrame
    channel_performance: pd.DataFrame
    geo_week_outcome: pd.DataFrame


def transform(data: pd.DataFrame) -> TransformResult:
    """Build dimensions and facts while preserving zero and missing semantics."""
    missing = sorted(set(EXPECTED_COLUMNS) - set(data.columns))
    if missing:
        raise TransformationError(f"Missing source columns: {missing}")
    frame = data.copy()
    parsed = pd.to_datetime(frame["time"], errors="coerce")
    if parsed.isna().any():
        raise TransformationError("One or more source dates cannot be parsed.")
    if frame.duplicated(["geo", "time"]).any():
        raise TransformationError("Duplicate geography-week keys are not loadable.")
    if frame["geo"].isna().any() or frame["geo"].astype(str).str.strip().eq("").any():
        raise TransformationError("Geography codes must be present and non-empty.")

    numeric = [column for column in EXPECTED_COLUMNS if column not in {"geo", "time"}]
    for column in numeric:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if frame[numeric].isna().any().any():
        raise TransformationError("Numeric source columns contain invalid or missing values.")
    non_negative = [
        column for column in numeric
        if column not in {"competitor_sales_control", "sentiment_score_control"}
    ]
    if (frame[non_negative] < 0).any().any():
        raise TransformationError("Non-negative source metrics contain negative values.")

    frame["_date_key"] = parsed.dt.date
    frame["_source_row_number"] = np.arange(1, len(frame) + 1, dtype=np.int64)
    staging = frame.rename(
        columns={
            "Unnamed: 0": "source_index",
            "geo": "geo_code",
            "time": "source_time",
            "_source_row_number": "source_row_number",
        }
    )[
        ["source_row_number", "source_index", "geo_code", "source_time"]
        + [column for column in EXPECTED_COLUMNS
           if column not in {"Unnamed: 0", "geo", "time"}]
    ]
    geography = pd.DataFrame({"geo_code": sorted(frame["geo"].astype(str).unique())})
    dates = pd.DataFrame({"date_key": sorted(frame["_date_key"].unique())})
    dates["source_week_date"] = dates["date_key"]
    dates["calendar_year"] = pd.to_datetime(dates["date_key"]).dt.year
    dates["calendar_month"] = pd.to_datetime(dates["date_key"]).dt.month
    dates["calendar_quarter"] = pd.to_datetime(dates["date_key"]).dt.quarter
    dates["calendar_week"] = pd.to_datetime(dates["date_key"]).dt.isocalendar().week.astype(int)
    channels = pd.DataFrame({
        "channel_code": PAID_CHANNELS + [ORGANIC_CHANNEL],
        "channel_type": ["paid"] * len(PAID_CHANNELS) + ["organic"],
    })

    channel_rows: list[dict[str, object]] = []
    for _, row in frame.iterrows():
        source_row_number = int(row["_source_row_number"])
        for channel in PAID_CHANNELS:
            channel_rows.append({
                "geo_code": row["geo"],
                "date_key": row["_date_key"],
                "channel_code": channel,
                "channel_type": "paid",
                "spend": row[f"{channel}_spend"],
                "impressions": row[f"{channel}_impression"],
                "source_row_number": source_row_number,
            })
        channel_rows.append({
            "geo_code": row["geo"],
            "date_key": row["_date_key"],
            "channel_code": ORGANIC_CHANNEL,
            "channel_type": "organic",
            "spend": None,
            "impressions": row["Organic_channel0_impression"],
            "source_row_number": source_row_number,
        })
    channel_performance = pd.DataFrame(channel_rows)
    outcome = pd.DataFrame({
        "geo_code": frame["geo"].astype(str),
        "date_key": frame["_date_key"],
        "source_row_number": frame["_source_row_number"],
        "conversions": frame["conversions"],
        "revenue_per_conversion": frame["revenue_per_conversion"],
        "promo": frame["Promo"],
        "competitor_sales_control": frame["competitor_sales_control"],
        "sentiment_score_control": frame["sentiment_score_control"],
        "population": frame["population"],
    })
    if len(channel_performance) != len(frame) * 6:
        raise TransformationError("Channel fact does not contain six rows per source row.")
    return TransformResult(staging, geography, dates, channels, channel_performance, outcome)
