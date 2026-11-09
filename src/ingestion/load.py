"""Transactional, idempotent loading into the MySQL star schema."""

from __future__ import annotations

import hashlib
import logging
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sqlalchemy import Engine, text

from .transform import TransformResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoadResult:
    """Load statistics and batch identity."""

    ingestion_batch_id: int
    inserted: bool
    counts: dict[str, int]


def source_sha256(path: str | Path) -> str:
    """Return the SHA-256 checksum used for batch idempotency."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _records(frame: pd.DataFrame, columns: Iterable[str]) -> list[Mapping[str, object]]:
    selected = frame[list(columns)].astype(object).where(frame.notna(), None)
    return selected.to_dict(orient="records")


def load_result(engine: Engine, source_path: str | Path, result: TransformResult) -> LoadResult:
    """Load one source batch; a matching filename/checksum is a no-op."""
    filename = Path(source_path).name
    checksum = source_sha256(source_path)
    with engine.begin() as connection:
        existing = connection.execute(
            text(
                "SELECT ingestion_batch_id FROM ingestion_batch "
                "WHERE source_filename = :filename AND source_sha256 = :checksum "
                "ORDER BY ingestion_batch_id DESC LIMIT 1"
            ),
            {"filename": filename, "checksum": checksum},
        ).scalar()
        if existing is not None:
            logger.info("Batch already loaded; skipping batch %s", existing)
            return LoadResult(int(existing), False, {"staging": 0, "channel_performance": 0, "geo_week_outcome": 0})

        batch_id = connection.execute(
            text(
                "INSERT INTO ingestion_batch "
                "(source_filename, source_sha256, source_row_count, validation_status) "
                "VALUES (:filename, :checksum, :row_count, 'passed')"
            ),
            {"filename": filename, "checksum": checksum, "row_count": len(result.staging)},
        ).lastrowid
        if batch_id is None:
            raise RuntimeError("MySQL did not return an ingestion batch identifier.")

        staging = result.staging.copy()
        staging["ingestion_batch_id"] = int(batch_id)
        staging_columns = [
            "ingestion_batch_id", "source_row_number", "source_index", "geo_code",
            "source_time", "Channel0_impression", "Channel1_impression",
            "Channel2_impression", "Channel3_impression", "Channel4_impression",
            "competitor_sales_control", "sentiment_score_control", "Channel0_spend",
            "Channel1_spend", "Channel2_spend", "Channel3_spend", "Channel4_spend",
            "Organic_channel0_impression", "Promo", "conversions",
            "revenue_per_conversion", "population",
        ]
        staging = staging[staging_columns]
        connection.execute(
            text(
                "INSERT INTO stg_marketing_geo_week "
                "(ingestion_batch_id, source_row_number, source_index, geo_code, source_time, "
                "channel0_impression, channel1_impression, channel2_impression, channel3_impression, "
                "channel4_impression, competitor_sales_control, sentiment_score_control, "
                "channel0_spend, channel1_spend, channel2_spend, channel3_spend, channel4_spend, "
                "organic_channel0_impression, promo, conversions, revenue_per_conversion, population) "
                "VALUES (:ingestion_batch_id, :source_row_number, :source_index, :geo_code, :source_time, "
                ":Channel0_impression, :Channel1_impression, :Channel2_impression, :Channel3_impression, "
                ":Channel4_impression, :competitor_sales_control, :sentiment_score_control, "
                ":Channel0_spend, :Channel1_spend, :Channel2_spend, :Channel3_spend, :Channel4_spend, "
                ":Organic_channel0_impression, :Promo, :conversions, :revenue_per_conversion, :population)"
            ),
            _records(staging, staging_columns),
        )
        connection.execute(
            text("INSERT INTO dim_geography (geo_code) VALUES (:geo_code) "
                 "ON DUPLICATE KEY UPDATE geo_code = VALUES(geo_code)"),
            _records(result.geography, ["geo_code"]),
        )
        connection.execute(
            text(
                "INSERT INTO dim_date (date_key, source_week_date, calendar_year, calendar_month, "
                "calendar_quarter, calendar_week) VALUES "
                "(:date_key, :source_week_date, :calendar_year, :calendar_month, "
                ":calendar_quarter, :calendar_week) "
                "ON DUPLICATE KEY UPDATE source_week_date = VALUES(source_week_date)"
            ),
            _records(result.dates, result.dates.columns),
        )
        connection.execute(
            text("INSERT INTO dim_channel (channel_code, channel_type) VALUES "
                 "(:channel_code, :channel_type) "
                 "ON DUPLICATE KEY UPDATE channel_type = VALUES(channel_type)"),
            _records(result.channels, result.channels.columns),
        )
        geo_keys = dict(connection.execute(text("SELECT geo_code, geography_key FROM dim_geography")).all())
        channel_keys = dict(connection.execute(text("SELECT channel_code, channel_key FROM dim_channel")).all())
        channel_rows = result.channel_performance.copy()
        channel_rows["geography_key"] = channel_rows["geo_code"].map(geo_keys)
        channel_rows["channel_key"] = channel_rows["channel_code"].map(channel_keys)
        channel_rows["ingestion_batch_id"] = int(batch_id)
        connection.execute(
            text(
                "INSERT INTO fact_channel_performance "
                "(geography_key, date_key, channel_key, ingestion_batch_id, source_row_number, spend, impressions) "
                "VALUES (:geography_key, :date_key, :channel_key, :ingestion_batch_id, "
                ":source_row_number, :spend, :impressions) "
                "ON DUPLICATE KEY UPDATE spend = VALUES(spend), impressions = VALUES(impressions), "
                "ingestion_batch_id = VALUES(ingestion_batch_id), source_row_number = VALUES(source_row_number)"
            ),
            _records(channel_rows, ["geography_key", "date_key", "channel_key", "ingestion_batch_id",
                                    "source_row_number", "spend", "impressions"]),
        )
        outcome = result.geo_week_outcome.copy()
        outcome["geography_key"] = outcome["geo_code"].map(geo_keys)
        outcome["ingestion_batch_id"] = int(batch_id)
        connection.execute(
            text(
                "INSERT INTO fact_geo_week_outcome "
                "(geography_key, date_key, ingestion_batch_id, source_row_number, conversions, "
                "revenue_per_conversion, promo, competitor_sales_control, sentiment_score_control, population) "
                "VALUES (:geography_key, :date_key, :ingestion_batch_id, :source_row_number, :conversions, "
                ":revenue_per_conversion, :promo, :competitor_sales_control, :sentiment_score_control, :population) "
                "ON DUPLICATE KEY UPDATE conversions = VALUES(conversions), "
                "revenue_per_conversion = VALUES(revenue_per_conversion), promo = VALUES(promo), "
                "competitor_sales_control = VALUES(competitor_sales_control), "
                "sentiment_score_control = VALUES(sentiment_score_control), population = VALUES(population), "
                "ingestion_batch_id = VALUES(ingestion_batch_id), source_row_number = VALUES(source_row_number)"
            ),
            _records(outcome, ["geography_key", "date_key", "ingestion_batch_id", "source_row_number",
                               "conversions", "revenue_per_conversion", "promo",
                               "competitor_sales_control", "sentiment_score_control", "population"]),
        )
    return LoadResult(int(batch_id), True, {
        "staging": len(result.staging),
        "channel_performance": len(result.channel_performance),
        "geo_week_outcome": len(result.geo_week_outcome),
    })
