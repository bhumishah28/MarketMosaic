# MarketMosaic Data Validation Report

**Dataset:** `data/raw/geo_all_channels.csv`  
**Validation implementation:** [`src/validation.py`](../src/validation.py)  
**Validation date:** November 7, 2026

## Dataset overview

The raw file contains **6,240 rows and 20 columns**. Its grain is one
geography-week observation: one `geo` and one weekly `time` value per row.
There are 40 geographies and 156 weekly periods from 2021-01-25 through
2024-01-15. The panel is balanced at 40 x 156 = 6,240 observations.

The raw file was not modified. The validator returns a report and does not
drop rows, impute values, or delete outliers.

## Schema and types

The observed CSV types are 18 numeric columns and two string columns:
`geo` and `time`. The full column-level definitions and current uncertainty
are in the [data dictionary](data_dictionary.md).

## Checks and results

| Check | Result |
|---|---:|
| Expected columns missing | 0 |
| Unexpected columns | 0 |
| Invalid observed data types | 0 |
| Missing cells | 0 |
| Exact duplicate rows | 0 |
| Duplicate `geo` + `time` keys | 0 |
| Invalid or unparseable dates | 0 |
| Unexpected weekly gaps | 0 |
| Geographies present / expected | 40 / 40 |
| Incomplete geography panels | 0 |
| Dates with incomplete geography coverage | 0 |
| Negative values in unambiguously non-negative fields | 0 |
| Spend/impression zero-state mismatches | 0 |
| Exported index sequence check | Passed (0–6,239) |

### Zero activity

Zero activity is retained as a valid observation, not treated as missing or
invalid. Zero spend rows are: Channel0 **755**, Channel1 **1,742**, Channel2
**4,010**, Channel3 **169**, and Channel4 **820**. For every paid channel,
zero spend and zero impressions occur together in the raw data. Channel2 is
zero-heavy (4,010 of 6,240 rows, 64.26%) and should be handled deliberately in
later modelling.

### Negative and definition-dependent values

The validator enforces non-negativity for the index, impressions, spend,
organic impressions, promotion, conversions, revenue-per-conversion, and
population. No violations were found. `competitor_sales_control` and
`sentiment_score_control` contain negative values (3,238 and 3,216 rows
respectively); these fields are not rejected because their scales and
baselines are not established by the source. Their negative values must be
confirmed before business interpretation.

### Outlier screening

The IQR screen flagged observations for investigation, not deletion:

| Field | Flagged rows |
|---|---:|
| Channel0 impression / spend | 164 |
| Channel1 impression / spend | 215 |
| Channel2 impression / spend | 941 |
| Channel3 impression / spend | 108 |
| Channel4 impression / spend | 143 |
| Organic_channel0_impression | 305 |
| Promo | 248 |
| conversions | 56 |
| revenue_per_conversion | 43 |
| competitor_sales_control | 61 |
| sentiment_score_control | 61 |
| population | 0 |

The paired impression and spend counts are equal because activity is generated
as a paired zero/non-zero state. These are statistical screening flags only;
the validator preserves all observations.

## Handling decisions

* The raw CSV remains the immutable source.
* `Unnamed: 0` is documented as an exported row index and should be excluded
  from modelling, rather than interpreted as a predictor.
* No zeros, negative control values, or outliers were automatically removed.
* Date parsing and panel checks are explicit and reusable.
* Validation failure can be returned as a report or raised with
  `validate_dataset(..., raise_on_error=True)`.

## Outstanding assumptions and questions

The source does not establish units or precise business definitions for the
simulated measures. Confirmation is needed for channel naming, spend and
impression units, conversions, `revenue_per_conversion`, `Promo`, both
controls, and the meaning of `Organic_channel0_impression`. It is also not yet
confirmed whether the negative controls are centred/indexed measures or have
another valid scale.

## Readiness

The dataset passes all mechanical validation checks and is ready for the next
engineering phase **as a validated raw analytical input**. It is not yet ready
for causal interpretation or production modelling until the outstanding
definitions and units are confirmed. The next phase should create an explicit
modelling preparation specification, including treatment of the index artifact,
zero-heavy channels, controls, and outlier review.
