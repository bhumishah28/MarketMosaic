"""Command-line orchestration for extraction, transformation, and loading."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

try:
    from validation import validate_dataset
except ModuleNotFoundError:
    from src.validation import validate_dataset

from ..database.connection import create_database_engine
from .extract import extract_csv
from .load import load_result
from .transform import transform

logger = logging.getLogger(__name__)


def run_pipeline(source_path: str | Path, dry_run: bool = False) -> int:
    """Run ETL and return 0 for success, 2 for a user/data/database failure."""
    try:
        extracted = extract_csv(source_path)
        validation = validate_dataset(extracted.drop(columns=["time_dt"]))
        if not validation["passed"]:
            logger.error("Source validation failed: %s", validation)
            return 2
        transformed = transform(extracted)
        logger.info(
            "Reconciled source rows=%d, geographies=%d, dates=%d, channels=%d, "
            "channel facts=%d, outcomes=%d",
            len(extracted), len(transformed.geography), len(transformed.dates),
            len(transformed.channels), len(transformed.channel_performance),
            len(transformed.geo_week_outcome),
        )
        if dry_run:
            return 0
        engine = create_database_engine()
        load_result(engine, source_path, transformed)
        engine.dispose()
        return 0
    except (OSError, ValueError, RuntimeError, SQLAlchemyError) as exc:
        logger.error("ETL pipeline failed: %s", exc)
        return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="data/raw/geo_all_channels.csv")
    parser.add_argument("--dry-run", action="store_true", help="Extract and transform without MySQL.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    return run_pipeline(args.source, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
