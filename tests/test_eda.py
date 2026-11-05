from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from eda import (
    SPEND_COLUMNS,
    channel_summary,
    correlation_matrix,
    data_quality_report,
    geography_summary,
    load_and_prepare_data,
    temporal_summary,
)


DATA_PATH = Path("data/raw/geo_all_channels.csv")


def test_real_dataset_preparation_and_quality():
    data = load_and_prepare_data(DATA_PATH)
    quality = data_quality_report(data)

    assert data.shape == (6240, 21)
    assert data["time_dt"].notna().all()
    assert quality["missing_cells"] == 0
    assert quality["exact_duplicates"] == 0
    assert quality["geo_time_duplicates"] == 0
    assert quality["unnamed_is_zero_based_sequence"] is True


def test_channel_summary_contains_all_five_channels():
    data = load_and_prepare_data(DATA_PATH)
    summary = channel_summary(data)

    assert summary.index.tolist() == ["Channel0", "Channel1", "Channel2", "Channel3", "Channel4"]
    assert summary.loc["Channel3", "spend_mean"] > summary.loc["Channel2", "spend_mean"]
    assert summary["spend_conversions_correlation"].between(-1, 1).all()


def test_geography_and_temporal_panel_shape():
    data = load_and_prepare_data(DATA_PATH)
    geo = geography_summary(data)
    weekly = temporal_summary(data)

    assert len(geo) == 40
    assert len(weekly) == 156
    assert geo["observations"].eq(156).all()
    assert weekly["total_spend"].ge(0).all()


def test_correlation_matrix_has_spend_and_outcome():
    data = load_and_prepare_data(DATA_PATH)
    matrix = correlation_matrix(data)

    assert matrix.shape == (6, 6)
    assert set(SPEND_COLUMNS + ["conversions"]) == set(matrix.columns)
