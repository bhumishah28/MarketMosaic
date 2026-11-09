import pandas as pd
import pytest

from src.ingestion.extract import extract_csv
from src.ingestion.load import source_sha256
from src.ingestion.transform import ORGANIC_CHANNEL, transform


def make_source() -> pd.DataFrame:
    rows = []
    for index, date in enumerate(("2024-01-01", "2024-01-08")):
        rows.append({
            "Unnamed: 0": index, "geo": "Geo0", "time": date,
            **{f"Channel{i}_impression": 100 + i for i in range(5)},
            "competitor_sales_control": -1.5, "sentiment_score_control": 0.2,
            **{f"Channel{i}_spend": 0.0 if i == 2 else 10.0 + i for i in range(5)},
            "Organic_channel0_impression": 55, "Promo": 0.0,
            "conversions": 3.0 + index, "revenue_per_conversion": 2.0,
            "population": 1000.0,
        })
    return pd.DataFrame(rows)


def test_extraction_adds_date_helper_without_rewriting_source(tmp_path):
    source = make_source()
    path = tmp_path / "source.csv"
    source.to_csv(path, index=False)
    extracted = extract_csv(path)
    assert extracted["time"].tolist() == source["time"].tolist()
    assert extracted["time_dt"].notna().all()


def test_transform_creates_six_channel_rows_per_observation():
    result = transform(make_source())
    assert len(result.channel_performance) == 12
    assert result.channels["channel_code"].tolist()[-1] == ORGANIC_CHANNEL
    assert result.channel_performance["channel_code"].nunique() == 6


def test_organic_channel_has_null_spend_and_keeps_impressions():
    organic = transform(make_source()).channel_performance.query(
        "channel_code == @ORGANIC_CHANNEL"
    )
    assert organic["spend"].isna().all()
    assert organic["impressions"].eq(55).all()


def test_zero_spend_and_signed_controls_are_preserved():
    result = transform(make_source())
    paid = result.channel_performance.query("channel_code == 'Channel2'")
    assert paid["spend"].eq(0).all()
    assert result.geo_week_outcome["competitor_sales_control"].eq(-1.5).all()


def test_duplicate_geo_week_is_rejected():
    source = pd.concat([make_source(), make_source().iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="Duplicate"):
        transform(source)


def test_output_keys_and_counts_reconcile():
    result = transform(make_source())
    assert len(result.staging) == len(result.geo_week_outcome) == 2
    assert len(result.geography) == 1
    assert len(result.dates) == 2
    assert result.channel_performance["source_row_number"].value_counts().eq(6).all()


def test_source_checksum_is_stable(tmp_path):
    path = tmp_path / "source.csv"
    path.write_bytes(b"stable source")
    assert source_sha256(path) == source_sha256(path)
