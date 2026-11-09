# MySQL Execution and ETL Verification

Date: 2026-11-09

## Environment

- MySQL Windows service: `MySQL80`, running.
- TCP endpoint: `localhost:3306`, reachable.
- Authentication: verified by MySQL Workbench and the project environment
  configuration.
- DDL execution: completed through SQLAlchemy/PyMySQL.
- No credentials are recorded in this report.

## Schema verification

The existing `sql/001_create_schema.sql` was executed without destructive
operations. Verified base tables:

`ingestion_batch`, `stg_marketing_geo_week`, `dim_geography`, `dim_date`,
`dim_channel`, `fact_channel_performance`, and `fact_geo_week_outcome`.

Verified view: `vw_geo_week_wide`.

## Loaded row counts

| Object | Rows |
|---|---:|
| ingestion_batch | 1 |
| stg_marketing_geo_week | 6,240 |
| dim_geography | 40 |
| dim_date | 156 |
| dim_channel | 6 |
| fact_channel_performance | 37,440 |
| fact_geo_week_outcome | 6,240 |
| vw_geo_week_wide | 6,240 |

## Reconciliation

| Metric | Source | MySQL |
|---|---:|---:|
| Conversions | 65,930,714,112.78999 | 65,930,714,112.79000000 |
| Paid spend | 219,492,402.35048598 | 219,492,402.35048597 |
| Paid impressions | 27,797,718,175 | 27,797,718,175 |
| Organic impressions | 3,322,592,024 | 3,322,592,024 |

Duplicate geography-date-channel and geography-date outcome keys both returned
zero rows. All 6,240 organic fact rows preserve `NULL` spend.

## Idempotency

Re-running the same source batch was detected by filename and SHA-256 checksum
and skipped without increasing fact or staging row counts.

## Analytical SQL

All statements in `sql/analytics/` executed successfully:

- Channel performance: 6 rows.
- Quarter-over-quarter and running weekly trends: 13 and 156 rows.
- Geography ranking, zero-spend frequency, and promotion analysis: 40, 5, and
  2 rows respectively.
