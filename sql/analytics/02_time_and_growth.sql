-- MySQL 8.x weekly trends, running spend, and quarter-over-quarter growth.

WITH weekly AS (
    SELECT
        dates.date_key,
        dates.weekly_paid_spend,
        outcomes.weekly_conversions
    FROM (
        SELECT f.date_key, SUM(f.spend) AS weekly_paid_spend
        FROM fact_channel_performance AS f
        JOIN dim_channel AS c ON c.channel_key = f.channel_key
        WHERE c.channel_type = 'paid'
        GROUP BY f.date_key
    ) AS dates
    JOIN (
        SELECT date_key, SUM(conversions) AS weekly_conversions
        FROM fact_geo_week_outcome
        GROUP BY date_key
    ) AS outcomes ON outcomes.date_key = dates.date_key
),
quarterly AS (
    SELECT
        YEAR(date_key) AS calendar_year,
        QUARTER(date_key) AS calendar_quarter,
        SUM(weekly_conversions) AS quarterly_conversions
    FROM weekly
    GROUP BY YEAR(date_key), QUARTER(date_key)
)
SELECT
    calendar_year,
    calendar_quarter,
    quarterly_conversions,
    LAG(quarterly_conversions) OVER (
        ORDER BY calendar_year, calendar_quarter
    ) AS prior_quarter_conversions,
    quarterly_conversions - LAG(quarterly_conversions) OVER (
        ORDER BY calendar_year, calendar_quarter
    ) AS qoq_change
FROM quarterly
ORDER BY calendar_year, calendar_quarter;

WITH weekly AS (
    SELECT
        dates.date_key,
        dates.weekly_paid_spend,
        outcomes.weekly_conversions
    FROM (
        SELECT f.date_key, SUM(f.spend) AS weekly_paid_spend
        FROM fact_channel_performance AS f
        JOIN dim_channel AS c ON c.channel_key = f.channel_key
        WHERE c.channel_type = 'paid'
        GROUP BY f.date_key
    ) AS dates
    JOIN (
        SELECT date_key, SUM(conversions) AS weekly_conversions
        FROM fact_geo_week_outcome
        GROUP BY date_key
    ) AS outcomes ON outcomes.date_key = dates.date_key
)
SELECT
    date_key,
    weekly_paid_spend,
    weekly_conversions,
    SUM(weekly_paid_spend) OVER (
        ORDER BY date_key ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_paid_spend
FROM weekly
ORDER BY date_key;
