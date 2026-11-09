-- MySQL 8.x channel-level performance summaries.

WITH channel_totals AS (
    SELECT
        c.channel_code,
        c.channel_type,
        SUM(COALESCE(f.spend, 0)) AS total_spend,
        SUM(COALESCE(f.impressions, 0)) AS total_impressions,
        SUM(f.spend IS NULL) AS null_spend_rows,
        SUM(f.spend = 0) AS zero_spend_rows
    FROM fact_channel_performance AS f
    JOIN dim_channel AS c ON c.channel_key = f.channel_key
    GROUP BY c.channel_code, c.channel_type
)
SELECT
    channel_code,
    channel_type,
    total_spend,
    total_impressions,
    null_spend_rows,
    zero_spend_rows,
    RANK() OVER (ORDER BY total_spend DESC) AS spend_rank
FROM channel_totals
ORDER BY spend_rank, channel_code;
