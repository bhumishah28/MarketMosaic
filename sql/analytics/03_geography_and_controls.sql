-- MySQL 8.x geography, zero-spend, promotion, and population-normalised analysis.

WITH geography_totals AS (
    SELECT
        g.geo_code,
        SUM(o.conversions) AS total_conversions,
        MAX(o.population) AS population,
        SUM(o.conversions) / NULLIF(MAX(o.population), 0) AS conversions_per_person
    FROM fact_geo_week_outcome AS o
    JOIN dim_geography AS g ON g.geography_key = o.geography_key
    GROUP BY g.geo_code
)
SELECT
    geo_code,
    total_conversions,
    population,
    conversions_per_person,
    RANK() OVER (ORDER BY conversions_per_person DESC) AS normalised_rank
FROM geography_totals
ORDER BY normalised_rank, geo_code;

SELECT
    c.channel_code,
    SUM(f.spend = 0) AS zero_spend_observations,
    COUNT(*) AS observations,
    SUM(f.spend = 0) / COUNT(*) AS zero_spend_rate
FROM fact_channel_performance AS f
JOIN dim_channel AS c ON c.channel_key = f.channel_key
WHERE c.channel_type = 'paid'
GROUP BY c.channel_code
ORDER BY zero_spend_rate DESC, c.channel_code;

SELECT
    CASE WHEN o.promo > 0 THEN 'promotion' ELSE 'no_promotion' END AS promotion_group,
    COUNT(*) AS geo_week_observations,
    AVG(o.conversions) AS mean_conversions,
    SUM(o.conversions) AS total_conversions
FROM fact_geo_week_outcome AS o
GROUP BY CASE WHEN o.promo > 0 THEN 'promotion' ELSE 'no_promotion' END
ORDER BY promotion_group;
