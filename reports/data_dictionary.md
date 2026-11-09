# MarketMosaic Data Dictionary

**Source:** `data/raw/geo_all_channels.csv`  
**Observed types:** captured from the raw CSV on November 7, 2026

“Unknown — requires confirmation” is used where the CSV and project source do
not establish a business definition or unit.

| Column | Observed type | Known meaning | Unit |
|---|---|---|---|
| `Unnamed: 0` | integer | Exported zero-based row index; not a business measure | None; index artifact |
| `geo` | string | Geography identifier | Unknown — requires confirmation |
| `time` | string | Weekly observation date | Date; calendar convention requires confirmation |
| `Channel0_impression` | integer | Paid media impressions for Channel0 | Unknown — requires confirmation |
| `Channel1_impression` | integer | Paid media impressions for Channel1 | Unknown — requires confirmation |
| `Channel2_impression` | integer | Paid media impressions for Channel2 | Unknown — requires confirmation |
| `Channel3_impression` | integer | Paid media impressions for Channel3 | Unknown — requires confirmation |
| `Channel4_impression` | integer | Paid media impressions for Channel4 | Unknown — requires confirmation |
| `competitor_sales_control` | decimal | Competitor-related control variable | Unknown — requires confirmation |
| `sentiment_score_control` | decimal | Sentiment-related control variable | Unknown — requires confirmation |
| `Channel0_spend` | decimal | Paid media spend for Channel0 | Unknown — requires confirmation |
| `Channel1_spend` | decimal | Paid media spend for Channel1 | Unknown — requires confirmation |
| `Channel2_spend` | decimal | Paid media spend for Channel2 | Unknown — requires confirmation |
| `Channel3_spend` | decimal | Paid media spend for Channel3 | Unknown — requires confirmation |
| `Channel4_spend` | decimal | Paid media spend for Channel4 | Unknown — requires confirmation |
| `Organic_channel0_impression` | integer | Organic impressions associated with Channel0 | Unknown — requires confirmation |
| `Promo` | decimal | Promotion-related feature | Unknown — requires confirmation |
| `conversions` | decimal | Outcome measure labelled conversions | Unknown — requires confirmation |
| `revenue_per_conversion` | decimal | Revenue-related measure per conversion | Unknown — requires confirmation |
| `population` | decimal | Geography population / market-size control | Unknown — requires confirmation |

## Interpretation notes

* `geo` and `time` form the observed row key; the raw data contains one row
  for each of 40 geographies across 156 weekly dates.
* Paid spend and impression pairs have matching zero states in the current
  file. Zero activity is therefore a valid observed state, not missing data.
* The two control variables include negative values. This is not classified as
  an error because their scale and baseline are unknown.
* The dictionary intentionally does not infer currencies, impression units,
  conversion definitions, or whether `revenue_per_conversion` is a currency
  amount, ratio, or simulated index.
