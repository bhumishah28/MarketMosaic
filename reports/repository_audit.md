# Repository Audit

Date: 2026-11-09

## Scope and method

The project root, Python modules, SQL DDL, tests, notebook metadata/code cells,
Markdown reports, configuration, dependency manifests, raw-data metadata, and
Git status/history were inspected. The raw CSV was inspected by schema and
aggregate metadata rather than printed in full.

## Classification

### 1. Essential and working

- `src/validation.py` — reusable validation checks; covered by tests.
- `src/eda.py` — EDA helpers; covered by tests.
- `src/inspect_data.py` — source inspection helpers; covered by tests.
- `tests/` — 31 baseline tests passed before this implementation.
- `data/raw/geo_all_channels.csv` — immutable source dataset (6,240 rows, 20 columns).
- `notebooks/eda_week1.ipynb` — existing exploratory work.
- Existing data-audit, dictionary, validation, modelling-readiness, and database-design reports.
- `sql/001_create_schema.sql` — MySQL 8.x DDL with dimensions, facts, lineage,
  constraints, indexes, and the wide view.

### 2. Essential but needing modifications

- `README.md` — corrected the stale PostgreSQL technology reference and documented
  the implemented ETL entry point.
- `pyproject.toml` and `requirements.txt` — added SQLAlchemy, PyMySQL,
  python-dotenv, and Ruff dependencies.
- `src/ingestion/` and `src/database/` — added as the production ETL/database layer.
- `tests/test_etl.py` — added focused transformation and reconciliation tests.

### 3. Redundant or duplicated

No verified duplicate implementation was found. `src/inspect_data.py` and
`src/validation.py` have different responsibilities and are both referenced by
tests, so neither was removed.

### 4. Generated and disposable

Existing `.pytest_cache`, Python caches, and notebook checkpoint locations are
generated artifacts. No tracked useful file was deleted during this audit.

### 5. Uncertain — needs human review

- Historical work reports may become stale as the ETL milestone advances; they
  were retained rather than rewritten.
- `docs/` is currently empty and has no referenced implementation.
- The notebook contains exploratory logic intentionally not duplicated in `src/`.

## Data and database findings

- The source has 6,240 rows, 40 geographies, 156 dates, and no null cells or
  duplicate `geo`/`time` keys.
- It contains five paid channel spend/impression pairs and one organic impressions
  field; it contains no organic spend field.
- The existing DDL is MySQL 8.x oriented and contains no `DROP`, `TRUNCATE`, or
  `DELETE` statements.
- The Windows `MySQL80` service is running and `localhost:3306` accepts TCP
  connections. The MySQL CLI binaries are not on PATH, and Workbench
  credentials/schema execution have not been verified, so live DDL execution
  is not claimed.
