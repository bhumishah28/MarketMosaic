"""Reusable validation checks for the raw MarketMosaic panel dataset."""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence

import pandas as pd
from pandas.api.types import is_numeric_dtype


EXPECTED_COLUMNS = [
    "Unnamed: 0",
    "geo",
    "time",
    "Channel0_impression",
    "Channel1_impression",
    "Channel2_impression",
    "Channel3_impression",
    "Channel4_impression",
    "competitor_sales_control",
    "sentiment_score_control",
    "Channel0_spend",
    "Channel1_spend",
    "Channel2_spend",
    "Channel3_spend",
    "Channel4_spend",
    "Organic_channel0_impression",
    "Promo",
    "conversions",
    "revenue_per_conversion",
    "population",
]
NUMERIC_COLUMNS = [column for column in EXPECTED_COLUMNS if column not in {"geo", "time"}]
NON_NEGATIVE_COLUMNS = [
    column
    for column in NUMERIC_COLUMNS
    if column not in {"competitor_sales_control", "sentiment_score_control"}
]
SPEND_COLUMNS = [f"Channel{index}_spend" for index in range(5)]
IMPRESSION_COLUMNS = [f"Channel{index}_impression" for index in range(5)]
ACTIVITY_PAIRS = list(zip(SPEND_COLUMNS, IMPRESSION_COLUMNS))


@dataclass
class ValidationResult:
    """A check result with a count and a human-readable description."""

    count: int
    passed: bool
    message: str

    def as_dict(self) -> Dict[str, object]:
        return {
            "count": self.count,
            "passed": self.passed,
            "message": self.message,
        }


class ValidationError(ValueError):
    """Raised when a dataset fails requested validation checks."""


def _result(count: int, message: str) -> ValidationResult:
    return ValidationResult(count=count, passed=count == 0, message=message)


def validate_schema(
    data: pd.DataFrame, expected_columns: Sequence[str] = EXPECTED_COLUMNS
) -> Dict[str, object]:
    """Check required columns and report unexpected columns without changing data."""
    expected = set(expected_columns)
    actual = set(data.columns)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    return {
        "missing_columns": missing,
        "unexpected_columns": unexpected,
        "passed": not missing and not unexpected,
    }


def validate_data_types(data: pd.DataFrame) -> Dict[str, object]:
    """Check numeric, geography, and date representations used by the raw schema."""
    missing = [column for column in EXPECTED_COLUMNS if column not in data]
    numeric_errors = [
        column
        for column in NUMERIC_COLUMNS
        if column in data and not is_numeric_dtype(data[column])
    ]
    categorical_error = (
        "geo"
        if "geo" in data and not (
            data["geo"].dtype == object
            or pd.api.types.is_string_dtype(data["geo"])
            or pd.api.types.is_categorical_dtype(data["geo"])
        )
        else None
    )
    date_error = (
        "time"
        if "time" in data
        and not (
            pd.api.types.is_string_dtype(data["time"])
            or pd.api.types.is_datetime64_any_dtype(data["time"])
        )
        else None
    )
    errors = numeric_errors + ([categorical_error] if categorical_error else [])
    errors += [date_error] if date_error else []
    errors += missing
    return {"invalid_columns": sorted(errors), "passed": not errors}


def validate_dates(data: pd.DataFrame) -> Dict[str, object]:
    """Check that every date parses and that sorted dates are seven days apart."""
    if "time" not in data:
        return {"invalid_dates": len(data), "gaps": [], "passed": False}
    parsed = pd.to_datetime(data["time"], errors="coerce")
    invalid = int(parsed.isna().sum())
    unique_dates = pd.Series(parsed.dropna().unique()).sort_values()
    gaps = [
        int(days)
        for days in unique_dates.diff().dropna().dt.days.tolist()
        if days != 7
    ]
    return {
        "invalid_dates": invalid,
        "gaps": gaps,
        "unexpected_gap_count": len(gaps),
        "passed": invalid == 0 and not gaps,
    }


def validate_panel(
    data: pd.DataFrame, expected_geographies: Optional[Iterable[str]] = None
) -> Dict[str, object]:
    """Check unique geo-week keys and balanced geography/date coverage."""
    required = {"geo", "time"}
    if not required.issubset(data.columns):
        return {"duplicate_keys": len(data), "passed": False}
    parsed = pd.to_datetime(data["time"], errors="coerce")
    key_data = data.assign(_parsed_time=parsed)
    duplicate_keys = int(data.duplicated(["geo", "time"]).sum())
    geo_counts = data.groupby("geo").size()
    date_counts = key_data.groupby("_parsed_time").size()
    expected = set(expected_geographies) if expected_geographies is not None else set(data["geo"].dropna())
    missing_geographies = sorted(expected - set(data["geo"].dropna()))
    expected_periods = len(parsed.dropna().unique())
    incomplete_geographies = sorted(
        str(geo) for geo, count in geo_counts.items() if count != expected_periods
    )
    unexpected_date_counts = int((date_counts != len(expected)).sum())
    return {
        "duplicate_keys": duplicate_keys,
        "geography_count": int(data["geo"].nunique()),
        "period_count": expected_periods,
        "missing_geographies": missing_geographies,
        "incomplete_geographies": incomplete_geographies,
        "unexpected_date_coverage": unexpected_date_counts,
        "passed": (
            duplicate_keys == 0
            and not missing_geographies
            and not incomplete_geographies
            and unexpected_date_counts == 0
        ),
    }


def validate_non_negative(data: pd.DataFrame) -> Dict[str, object]:
    """Find negative values only in fields where non-negativity is unambiguous."""
    counts = {
        column: int((data[column] < 0).sum())
        for column in NON_NEGATIVE_COLUMNS
        if column in data and is_numeric_dtype(data[column])
    }
    return {
        "negative_counts": counts,
        "negative_total": sum(counts.values()),
        "passed": sum(counts.values()) == 0,
    }


def validate_activity_pairs(data: pd.DataFrame) -> Dict[str, object]:
    """Report spend/impression mismatches without assuming zero activity is invalid."""
    mismatches = {}
    for spend, impression in ACTIVITY_PAIRS:
        if spend in data and impression in data:
            mismatches[f"{spend}/{impression}"] = int(
                ((data[spend] == 0) != (data[impression] == 0)).sum()
            )
    return {
        "mismatch_counts": mismatches,
        "zero_activity_counts": {
            spend: int((data[spend] == 0).sum())
            for spend in SPEND_COLUMNS
            if spend in data
        },
        "passed": sum(mismatches.values()) == 0,
        "message": "Zero activity is reported, not rejected.",
    }


def validate_index_column(data: pd.DataFrame) -> Dict[str, object]:
    """Check whether ``Unnamed: 0`` is an exported zero-based row index."""
    if "Unnamed: 0" not in data:
        return {"present": False, "is_zero_based_sequence": False, "passed": False}
    expected = pd.Series(range(len(data)), index=data.index)
    column = data["Unnamed: 0"]
    is_sequence = bool(column.equals(expected))
    return {
        "present": True,
        "unique": int(column.nunique()),
        "minimum": None if column.empty else column.min(),
        "maximum": None if column.empty else column.max(),
        "is_zero_based_sequence": is_sequence,
        "passed": is_sequence,
        "message": "Index artifact; exclude from modelling after preserving the raw file.",
    }


def flag_outliers(
    data: pd.DataFrame, columns: Optional[Iterable[str]] = None
) -> Dict[str, int]:
    """Return IQR screening counts; no rows are removed or modified."""
    selected = list(columns or NUMERIC_COLUMNS)
    flags = {}
    for column in selected:
        if column not in data or not is_numeric_dtype(data[column]):
            continue
        q1, q3 = data[column].quantile([0.25, 0.75])
        iqr = q3 - q1
        flags[column] = int(
            ((data[column] < q1 - 1.5 * iqr) | (data[column] > q3 + 1.5 * iqr)).sum()
        )
    return flags


def validate_dataset(
    data: pd.DataFrame,
    expected_geographies: Optional[Iterable[str]] = None,
    raise_on_error: bool = False,
) -> Dict[str, object]:
    """Run all checks and return a serialisable report without altering ``data``."""
    schema = validate_schema(data)
    types = validate_data_types(data)
    parsed = pd.to_datetime(data["time"], errors="coerce") if "time" in data else pd.Series(dtype="datetime64[ns]")
    date_report = validate_dates(data)
    panel = validate_panel(data, expected_geographies)
    negative = validate_non_negative(data)
    activity = validate_activity_pairs(data)
    index = validate_index_column(data)
    report = {
        "rows": len(data),
        "columns": len(data.columns),
        "missing_cells": int(data.isna().sum().sum()),
        "exact_duplicates": int(data.duplicated().sum()),
        "schema": schema,
        "data_types": types,
        "invalid_dates": date_report["invalid_dates"],
        "date_continuity": date_report,
        "panel": panel,
        "negative_values": negative,
        "activity": activity,
        "index_column": index,
        "outlier_flags": flag_outliers(data),
        "time_start": None if parsed.empty or parsed.dropna().empty else parsed.min().date().isoformat(),
        "time_end": None if parsed.empty or parsed.dropna().empty else parsed.max().date().isoformat(),
    }
    structural_failures = (
        report["missing_cells"] > 0
        or report["exact_duplicates"] > 0
        or not schema["passed"]
        or not types["passed"]
        or report["invalid_dates"] > 0
        or not date_report["passed"]
        or not panel["passed"]
        or not negative["passed"]
        or not activity["passed"]
        or not index["passed"]
    )
    report["passed"] = not structural_failures
    if raise_on_error and structural_failures:
        raise ValidationError("Dataset validation failed; inspect the returned report for failed checks.")
    return report
