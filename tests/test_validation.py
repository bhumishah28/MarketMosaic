from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from validation import (  # noqa: E402
    EXPECTED_COLUMNS,
    ValidationError,
    flag_outliers,
    validate_dataset,
)


def make_panel() -> pd.DataFrame:
    rows = []
    for geo in ("Geo0", "Geo1"):
        for index, date in enumerate(("2024-01-01", "2024-01-08", "2024-01-15")):
            row = {column: 0 for column in EXPECTED_COLUMNS}
            row.update(
                {
                    "geo": geo,
                    "time": date,
                    "Unnamed: 0": len(rows),
                    "population": 1000.0,
                    "conversions": 10.0 + index,
                    "revenue_per_conversion": 0.02,
                    "Channel0_impression": 100,
                    "Channel0_spend": 10.0,
                }
            )
            rows.append(row)
    return pd.DataFrame(rows, columns=EXPECTED_COLUMNS)


def test_valid_synthetic_panel_passes():
    report = validate_dataset(make_panel(), expected_geographies=["Geo0", "Geo1"])

    assert report["passed"] is True
    assert report["missing_cells"] == 0
    assert report["exact_duplicates"] == 0
    assert report["invalid_dates"] == 0
    assert report["date_continuity"]["unexpected_gap_count"] == 0


@pytest.mark.parametrize(
    "mutator, report_key",
    [
        (lambda frame: frame.drop(columns=["population"]), "schema"),
        (lambda frame: frame.assign(conversions="bad"), "data_types"),
        (lambda frame: frame.assign(population=None), "missing_cells"),
        (lambda frame: pd.concat([frame, frame.iloc[[0]]]), "exact_duplicates"),
        (
            lambda frame: frame.assign(time=frame["time"].where(frame.index != 1, "not-a-date")),
            "invalid_dates",
        ),
        (
            lambda frame: frame.assign(Channel0_spend=frame["Channel0_spend"].where(frame.index != 0, -1)),
            "negative_values",
        ),
    ],
)
def test_invalid_inputs_are_reported(mutator, report_key):
    report = validate_dataset(mutator(make_panel()))

    if report_key in {"schema", "data_types", "negative_values"}:
        assert report[report_key]["passed"] is False
    elif report_key == "missing_cells":
        assert report[report_key] == len(make_panel())
    else:
        assert report[report_key] > 0
    assert report["passed"] is False


def test_duplicate_geo_week_key_is_reported():
    data = make_panel()
    data.loc[1, "time"] = data.loc[0, "time"]

    report = validate_dataset(data)

    assert report["panel"]["duplicate_keys"] == 1
    assert report["passed"] is False


def test_missing_week_is_reported_without_deleting_rows():
    data = make_panel()
    data = data[data["time"] != "2024-01-08"].reset_index(drop=True)

    report = validate_dataset(data)

    assert report["date_continuity"]["unexpected_gap_count"] == 1
    assert len(data) == 4
    assert report["passed"] is False


def test_zero_activity_is_valid_and_reported():
    data = make_panel()
    data["Channel0_impression"] = 0
    data["Channel0_spend"] = 0

    report = validate_dataset(data)

    assert report["passed"] is True
    assert report["activity"]["zero_activity_counts"]["Channel0_spend"] == 6


def test_outlier_screen_flags_without_mutating_or_deleting_rows():
    data = make_panel()
    original = data.copy(deep=True)
    data.loc[0, "conversions"] = 10000

    flags = flag_outliers(data, ["conversions"])

    assert flags["conversions"] >= 1
    assert data.loc[0, "conversions"] == 10000
    pd.testing.assert_frame_equal(data.drop(index=0), original.drop(index=0))
    assert len(data) == len(original)


def test_exported_index_is_reported_as_artifact_and_raise_mode_is_explicit():
    data = make_panel()
    data.loc[0, "Unnamed: 0"] = 99

    report = validate_dataset(data)

    assert report["index_column"]["is_zero_based_sequence"] is False
    with pytest.raises(ValidationError):
        validate_dataset(data, raise_on_error=True)


def test_real_dataset_validation():
    path = Path("data/raw/geo_all_channels.csv")
    if not path.exists():
        pytest.skip("raw dataset is not available from this working directory")
    data = pd.read_csv(path)
    report = validate_dataset(data, expected_geographies=[f"Geo{i}" for i in range(40)])

    assert report["passed"] is True
    assert report["rows"] == 6240
