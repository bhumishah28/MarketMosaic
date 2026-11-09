# MarketMosaic Daily Work Report — 2026-11-08

## Objective

Implement the MySQL 8.x database architecture recommended by the modelling
readiness milestone, while preserving the raw CSV and deferring ETL,
modelling, forecasting, optimisation, dashboards, and deployment.

## Architecture implemented

The schema is a hybrid architecture:

- Raw-shaped staging for source preservation and lineage
- Long-format channel performance fact
- Separate geography-week outcome fact
- Geography, date, and generic channel dimensions
- Ingestion-batch metadata
- A wide analytical view for future matrix-shaped model inputs

The canonical analytical storage is long-format by geography, date, and
channel. Outcomes remain at geography-date grain to avoid duplication when
joining channel records.

## Files created or modified

Created:

- `sql/001_create_schema.sql`
- `reports/database_design.md`
- `reports/2026-11-08_work_report.md`

No existing source code, tests, notebooks, reports, or raw data were modified.

## Database tables and grains

- `ingestion_batch`: one row per source-file ingestion attempt.
- `stg_marketing_geo_week`: one row per source CSV row per ingestion batch.
- `dim_geography`: one row per generic source geography code.
- `dim_date`: one row per source weekly date.
- `dim_channel`: one row per generic source channel.
- `fact_channel_performance`: one row per geography-date-channel.
- `fact_geo_week_outcome`: one row per geography-date.
- `vw_geo_week_wide`: derived wide view with one row per geography-date.

The staging table retains all source fields, including the original
`Unnamed: 0` value as technical `source_index` lineage. It is not a modelling
feature.

## Keys, foreign keys, and indexes

- Dimension primary keys use surrogate keys except `dim_date`, which uses the
  source date as its primary key.
- Fact primary keys enforce their declared grains.
- Geography, date, and channel foreign keys enforce dimensional integrity.
- Composite staging lineage foreign keys connect fact rows back to their
  ingestion batch and source row.
- Unique constraints prevent duplicate dimension codes, staging rows, and
  source-lineage fact records.
- Indexes support date/channel, channel/geography, date/geography, staging
  lookup, and ingestion status queries.

## SQL execution and verification results

The environment was checked for `mysql` and `mysqld`. Neither executable was
available, so live MySQL execution was not performed. Consequently, no claim
is made that tables were created or inspected on a server.

The SQL file is written for MySQL 8.x using InnoDB, `utf8mb4`, foreign keys,
check constraints, and a MySQL-compatible view definition. The exact
environment-based command and post-execution inspection queries are documented
in `reports/database_design.md`.

No credentials, passwords, `.env` files, or connection configuration were
created.

## Data handling and unresolved assumptions

- Zero activity remains numeric zero.
- Organic spend is `NULL` because no organic spend source column exists; this
  does not invent a zero value.
- Negative competitor and sentiment control values are preserved.
- No source values are deleted or transformed.
- No units, currencies, platform mappings, geography names, or date-week
  conventions are invented.
- The exported index is retained only for source lineage.

Pending semantic questions include spend and impression units, outcome
definitions, control baselines, population timing, channel mappings, and the
source date convention.

## What remains pending

- Live execution against a MySQL 8.x development server
- Non-destructive CSV-to-staging loading
- Dimension and fact population
- Batch checksum and validation lifecycle implementation
- Schema integrity tests against a live or containerised database
- Wide-view data verification after loading

ETL, machine learning, MMM, forecasting, optimisation, dashboards, and
deployment remain outside this milestone.

## Exact next milestone

The next milestone is **schema-aware ingestion design and testing**:

1. Confirm the remaining source definitions and units.
2. Implement a non-destructive CSV-to-staging load.
3. Populate dimensions and both fact tables.
4. Add row-count, key, foreign-key, zero-state, and lineage tests.
5. Verify the wide modelling view against the source-shaped staging data.
