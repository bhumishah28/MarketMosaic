-- MarketMosaic MySQL 8.x schema
-- This file creates structure only. It does not load the CSV or create
-- derived model features.

CREATE DATABASE IF NOT EXISTS marketmosaic
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE marketmosaic;

CREATE TABLE IF NOT EXISTS ingestion_batch (
    ingestion_batch_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    source_filename VARCHAR(255) NOT NULL,
    source_sha256 CHAR(64) NULL,
    ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_row_count INT UNSIGNED NULL,
    validation_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    validation_message VARCHAR(1000) NULL,
    PRIMARY KEY (ingestion_batch_id),
    KEY ix_ingestion_batch_status (validation_status, ingested_at),
    CONSTRAINT chk_ingestion_batch_status
        CHECK (validation_status IN ('pending', 'passed', 'failed'))
) ENGINE = InnoDB
  COMMENT = 'Source-file lineage and validation metadata; no credentials are stored.';

CREATE TABLE IF NOT EXISTS stg_marketing_geo_week (
    ingestion_batch_id BIGINT UNSIGNED NOT NULL,
    source_row_number BIGINT UNSIGNED NOT NULL COMMENT 'Technical source row lineage, not a model feature.',
    source_index BIGINT SIGNED NULL COMMENT 'Original Unnamed: 0 value preserved from the CSV.',
    geo_code VARCHAR(64) NOT NULL,
    source_time VARCHAR(32) NOT NULL COMMENT 'Original time text preserved exactly.',
    channel0_impression BIGINT UNSIGNED NULL,
    channel1_impression BIGINT UNSIGNED NULL,
    channel2_impression BIGINT UNSIGNED NULL,
    channel3_impression BIGINT UNSIGNED NULL,
    channel4_impression BIGINT UNSIGNED NULL,
    competitor_sales_control DECIMAL(24, 8) NULL,
    sentiment_score_control DECIMAL(24, 8) NULL,
    channel0_spend DECIMAL(24, 8) NULL,
    channel1_spend DECIMAL(24, 8) NULL,
    channel2_spend DECIMAL(24, 8) NULL,
    channel3_spend DECIMAL(24, 8) NULL,
    channel4_spend DECIMAL(24, 8) NULL,
    organic_channel0_impression BIGINT UNSIGNED NULL,
    promo DECIMAL(24, 8) NULL,
    conversions DECIMAL(24, 8) NULL,
    revenue_per_conversion DECIMAL(24, 12) NULL,
    population DECIMAL(24, 8) NULL,
    PRIMARY KEY (ingestion_batch_id, source_row_number),
    KEY ix_stg_geo_time (geo_code, source_time),
    CONSTRAINT fk_stg_ingestion_batch
        FOREIGN KEY (ingestion_batch_id)
        REFERENCES ingestion_batch (ingestion_batch_id)
) ENGINE = InnoDB
  COMMENT = 'Raw-shaped staging structure; business units remain intentionally unspecified.';

CREATE TABLE IF NOT EXISTS dim_geography (
    geography_key BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    geo_code VARCHAR(64) NOT NULL,
    PRIMARY KEY (geography_key),
    UNIQUE KEY uq_dim_geography_code (geo_code)
) ENGINE = InnoDB
  COMMENT = 'Generic geography identifiers from the source; no locations are invented.';

CREATE TABLE IF NOT EXISTS dim_date (
    date_key DATE NOT NULL COMMENT 'Source weekly date; week-start/week-end semantics remain unconfirmed.',
    source_week_date DATE NOT NULL,
    calendar_year SMALLINT UNSIGNED NOT NULL,
    calendar_month TINYINT UNSIGNED NOT NULL,
    calendar_quarter TINYINT UNSIGNED NOT NULL,
    calendar_week TINYINT UNSIGNED NULL COMMENT 'Calendar convention must be confirmed before interpretation.',
    PRIMARY KEY (date_key),
    UNIQUE KEY uq_dim_date_source_week_date (source_week_date),
    CONSTRAINT chk_dim_date_month CHECK (calendar_month BETWEEN 1 AND 12),
    CONSTRAINT chk_dim_date_quarter CHECK (calendar_quarter BETWEEN 1 AND 4),
    CONSTRAINT chk_dim_date_week CHECK (calendar_week IS NULL OR calendar_week BETWEEN 1 AND 53)
) ENGINE = InnoDB
  COMMENT = 'Weekly date dimension with calendar attributes; no fiscal semantics are assumed.';

CREATE TABLE IF NOT EXISTS dim_channel (
    channel_key SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    channel_code VARCHAR(64) NOT NULL,
    channel_type VARCHAR(16) NOT NULL COMMENT 'Generic paid/organic classification from source field names.',
    PRIMARY KEY (channel_key),
    UNIQUE KEY uq_dim_channel_code (channel_code),
    CONSTRAINT chk_dim_channel_type CHECK (channel_type IN ('paid', 'organic'))
) ENGINE = InnoDB
  COMMENT = 'Generic source channel identifiers; platform names are not inferred.';

CREATE TABLE IF NOT EXISTS fact_channel_performance (
    geography_key BIGINT UNSIGNED NOT NULL,
    date_key DATE NOT NULL,
    channel_key SMALLINT UNSIGNED NOT NULL,
    ingestion_batch_id BIGINT UNSIGNED NOT NULL,
    source_row_number BIGINT UNSIGNED NOT NULL,
    spend DECIMAL(24, 8) NULL COMMENT 'NULL means not applicable, as for the organic channel.',
    impressions BIGINT UNSIGNED NULL,
    PRIMARY KEY (geography_key, date_key, channel_key),
    UNIQUE KEY uq_fact_channel_source_lineage
        (ingestion_batch_id, source_row_number, channel_key),
    KEY ix_fact_channel_date_channel (date_key, channel_key),
    KEY ix_fact_channel_channel_geo (channel_key, geography_key),
    CONSTRAINT fk_fact_channel_geography
        FOREIGN KEY (geography_key) REFERENCES dim_geography (geography_key),
    CONSTRAINT fk_fact_channel_date
        FOREIGN KEY (date_key) REFERENCES dim_date (date_key),
    CONSTRAINT fk_fact_channel_channel
        FOREIGN KEY (channel_key) REFERENCES dim_channel (channel_key),
    CONSTRAINT fk_fact_channel_batch
        FOREIGN KEY (ingestion_batch_id) REFERENCES ingestion_batch (ingestion_batch_id),
    CONSTRAINT fk_fact_channel_source
        FOREIGN KEY (ingestion_batch_id, source_row_number)
        REFERENCES stg_marketing_geo_week (ingestion_batch_id, source_row_number),
    CONSTRAINT chk_fact_channel_spend CHECK (spend IS NULL OR spend >= 0)
) ENGINE = InnoDB
  COMMENT = 'One geography-date-channel row; zero activity remains zero and non-applicable spend is NULL.';

CREATE TABLE IF NOT EXISTS fact_geo_week_outcome (
    geography_key BIGINT UNSIGNED NOT NULL,
    date_key DATE NOT NULL,
    ingestion_batch_id BIGINT UNSIGNED NOT NULL,
    source_row_number BIGINT UNSIGNED NOT NULL,
    conversions DECIMAL(24, 8) NULL,
    revenue_per_conversion DECIMAL(24, 12) NULL,
    promo DECIMAL(24, 8) NULL,
    competitor_sales_control DECIMAL(24, 8) NULL COMMENT 'Negative values are preserved.',
    sentiment_score_control DECIMAL(24, 8) NULL COMMENT 'Negative values are preserved.',
    population DECIMAL(24, 8) NULL,
    PRIMARY KEY (geography_key, date_key),
    UNIQUE KEY uq_fact_outcome_source_lineage
        (ingestion_batch_id, source_row_number),
    KEY ix_fact_outcome_date_geo (date_key, geography_key),
    KEY ix_fact_outcome_batch (ingestion_batch_id),
    CONSTRAINT fk_fact_outcome_geography
        FOREIGN KEY (geography_key) REFERENCES dim_geography (geography_key),
    CONSTRAINT fk_fact_outcome_date
        FOREIGN KEY (date_key) REFERENCES dim_date (date_key),
    CONSTRAINT fk_fact_outcome_batch
        FOREIGN KEY (ingestion_batch_id) REFERENCES ingestion_batch (ingestion_batch_id),
    CONSTRAINT fk_fact_outcome_source
        FOREIGN KEY (ingestion_batch_id, source_row_number)
        REFERENCES stg_marketing_geo_week (ingestion_batch_id, source_row_number),
    CONSTRAINT chk_fact_outcome_conversions
        CHECK (conversions IS NULL OR conversions >= 0),
    CONSTRAINT chk_fact_outcome_revenue
        CHECK (revenue_per_conversion IS NULL OR revenue_per_conversion >= 0),
    CONSTRAINT chk_fact_outcome_population
        CHECK (population IS NULL OR population >= 0)
) ENGINE = InnoDB
  COMMENT = 'One geography-date outcome row; controls retain their original signed values.';

CREATE OR REPLACE VIEW vw_geo_week_wide AS
SELECT
    o.geography_key,
    o.date_key,
    o.conversions,
    o.revenue_per_conversion,
    o.promo,
    o.competitor_sales_control,
    o.sentiment_score_control,
    o.population,
    MAX(CASE WHEN c.channel_code = 'Channel0' THEN f.spend END) AS channel0_spend,
    MAX(CASE WHEN c.channel_code = 'Channel1' THEN f.spend END) AS channel1_spend,
    MAX(CASE WHEN c.channel_code = 'Channel2' THEN f.spend END) AS channel2_spend,
    MAX(CASE WHEN c.channel_code = 'Channel3' THEN f.spend END) AS channel3_spend,
    MAX(CASE WHEN c.channel_code = 'Channel4' THEN f.spend END) AS channel4_spend,
    MAX(CASE WHEN c.channel_code = 'Channel0' THEN f.impressions END) AS channel0_impressions,
    MAX(CASE WHEN c.channel_code = 'Channel1' THEN f.impressions END) AS channel1_impressions,
    MAX(CASE WHEN c.channel_code = 'Channel2' THEN f.impressions END) AS channel2_impressions,
    MAX(CASE WHEN c.channel_code = 'Channel3' THEN f.impressions END) AS channel3_impressions,
    MAX(CASE WHEN c.channel_code = 'Channel4' THEN f.impressions END) AS channel4_impressions,
    MAX(CASE WHEN c.channel_code = 'Organic_channel0' THEN f.impressions END)
        AS organic_channel0_impressions
FROM fact_geo_week_outcome AS o
JOIN fact_channel_performance AS f
    ON f.geography_key = o.geography_key
   AND f.date_key = o.date_key
JOIN dim_channel AS c
    ON c.channel_key = f.channel_key
GROUP BY
    o.geography_key,
    o.date_key,
    o.conversions,
    o.revenue_per_conversion,
    o.promo,
    o.competitor_sales_control,
    o.sentiment_score_control,
    o.population;
