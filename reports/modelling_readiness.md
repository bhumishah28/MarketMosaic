# MarketMosaic Modelling Readiness Specification

**Dataset:** `data/raw/geo_all_channels.csv`  
**Prepared:** November 7, 2026  
**Scope:** Analytical investigation and modelling-readiness design only  
**Implementation status:** No preprocessing pipeline, model, database table, SQL
DDL, or ETL code is created by this document.

## 1. Executive summary

The source is a mechanically validated, simulated multi-geography marketing
panel. Each row is one geography-week observation. It contains 6,240 rows,
20 raw columns, 40 geographies, and 156 weekly dates from 2021-01-25 through
2024-01-15. Every geography has one observation for every date, and every date
has all 40 geographies.

The data is **ready for descriptive exploration** and **conditionally ready for
carefully scoped analytical preparation**. It is not automatically ready for
causal Marketing Mix Modelling, production forecasting, or budget
optimisation. Mechanical cleanliness does not establish:

- The units or business definitions of the variables
- Whether the controls are centred, indexed, or otherwise transformed
- Whether `conversions` is a count, rate, or simulated continuous outcome
- Whether `revenue_per_conversion` is currency, a ratio, or an index
- Whether the historical variation identifies causal channel response
- Whether the short 2024 tail is adequate for forecasting evaluation

The recommended immediate next step is a **modelling-preparation
specification review and business-definition confirmation**, followed by a
versioned preparation dataset. No raw observations should be deleted until
there is an explicit, documented business rule.

## 2. Dataset overview and grain

### 2.1 Confirmed structural facts

The validation report and raw file establish:

| Property | Observed result |
|---|---:|
| Rows | 6,240 |
| Raw columns | 20 |
| Geographies | 40 |
| Weekly periods | 156 |
| Date range | 2021-01-25 to 2024-01-15 |
| Expected panel size | 40 × 156 = 6,240 |
| Missing cells | 0 |
| Exact duplicate rows | 0 |
| Duplicate `geo` + `time` keys | 0 |
| Invalid dates | 0 |
| Unexpected weekly gaps | 0 |
| Incomplete geography panels | 0 |
| Incomplete date coverage | 0 |

The source README identifies this as Google's simulated Meridian marketing-mix
dataset. That provenance supports treating it as simulated MMM data, but it
does not provide project-specific units or a business glossary for every
column.

### 2.2 Row interpretation

**Confirmed:** `geo` and `time` form a unique observed row key, and the panel
is balanced.

**Analytical interpretation:** one row can be used as a geography-week unit for
panel summaries, exploratory regressions, or a future geo-week MMM input.
This does not by itself establish that each measure is a true causal exposure
or that all measures were generated under realistic operational rules.

### 2.3 Variable groups

| Group | Columns | Potential analytical role |
|---|---|---|
| Metadata / identifiers | `Unnamed: 0`, `geo`, `time` | Row identity, geography effects, temporal ordering |
| Paid activity | Five `Channel*_spend` and five `Channel*_impression` fields | Candidate media exposures |
| Organic activity | `Organic_channel0_impression` | Candidate non-paid activity exposure |
| Outcome | `conversions` | Candidate modelling target; definition requires confirmation |
| Revenue-related | `revenue_per_conversion` | Candidate outcome or secondary KPI; definition requires confirmation |
| Controls / context | `Promo`, `competitor_sales_control`, `sentiment_score_control` | Candidate covariates; scales require confirmation |
| Market size | `population` | Candidate geography-size control or normalisation denominator |

These are analytical roles, not claims that the source has confirmed a
business interpretation or causal direction.

## 3. Column-level semantic investigation

The table distinguishes the observed type from the potential modelling role.
Where the source does not establish meaning or units, the required wording is
used explicitly.

| Column | Data type | Potential business role | Confirmed meaning | Known unit | Observed characteristics | Open questions |
|---|---|---|---|---|---|---|
| `Unnamed: 0` | integer | Metadata / row-order identifier | Exported zero-based index; values run 0–6,239 | None; index artifact | Unique and sequential | Which export created it? Confirm it is not an operational key |
| `geo` | string | Geography identifier and panel effect | Geography label used in the dataset | Unknown — requires confirmation | 40 unique values, including labels such as `Geo0` | Do labels map to regions, markets, stores, or another entity? |
| `time` | string | Weekly time index | Date field for the weekly observations | Date; calendar convention requires confirmation | 156 unique dates, seven days apart | Is the date week-start, week-end, or reporting-period label? |
| `Channel0_impression` | integer | Paid-media exposure | Field labelled Channel0 impressions | Unknown — requires confirmation | 755 zeros; IQR flags: 164 | Are these served, viewable, or attributed impressions? |
| `Channel1_impression` | integer | Paid-media exposure | Field labelled Channel1 impressions | Unknown — requires confirmation | 1,742 zeros; IQR flags: 215 | What media platform and impression definition does Channel1 represent? |
| `Channel2_impression` | integer | Paid-media exposure | Field labelled Channel2 impressions | Unknown — requires confirmation | 4,010 zeros; IQR flags: 941 | Does zero mean inactive, unavailable, or unobserved activity? |
| `Channel3_impression` | integer | Paid-media exposure | Field labelled Channel3 impressions | Unknown — requires confirmation | 169 zeros; IQR flags: 108 | What is the channel and measurement window? |
| `Channel4_impression` | integer | Paid-media exposure | Field labelled Channel4 impressions | Unknown — requires confirmation | 820 zeros; IQR flags: 143 | What is the channel and measurement window? |
| `competitor_sales_control` | decimal | Market / competitor control | Field labelled competitor sales control | Unknown — requires confirmation | 3,238 negative values; 61 IQR flags | Is it centred, differenced, indexed, or otherwise transformed? |
| `sentiment_score_control` | decimal | Demand / sentiment control | Field labelled sentiment score control | Unknown — requires confirmation | 3,216 negative values; 61 IQR flags | What is the score range, baseline, source, and direction? |
| `Channel0_spend` | decimal | Paid-media investment exposure | Field labelled Channel0 spend | Unknown — requires confirmation | 755 zeros; IQR flags: 164; right-skewed | Currency, nominal/real basis, and spend attribution window? |
| `Channel1_spend` | decimal | Paid-media investment exposure | Field labelled Channel1 spend | Unknown — requires confirmation | 1,742 zeros; IQR flags: 215; right-skewed | Currency, nominal/real basis, and spend attribution window? |
| `Channel2_spend` | decimal | Paid-media investment exposure | Field labelled Channel2 spend | Unknown — requires confirmation | 4,010 zeros; IQR flags: 941; right-skewed | Is the sparsity an inactive-channel state by design? |
| `Channel3_spend` | decimal | Paid-media investment exposure | Field labelled Channel3 spend | Unknown — requires confirmation | 169 zeros; IQR flags: 108; largest mean spend in EDA | Currency, nominal/real basis, and spend attribution window? |
| `Channel4_spend` | decimal | Paid-media investment exposure | Field labelled Channel4 spend | Unknown — requires confirmation | 820 zeros; IQR flags: 143; right-skewed | Currency, nominal/real basis, and spend attribution window? |
| `Organic_channel0_impression` | integer | Organic activity exposure | Field labelled organic Channel0 impressions | Unknown — requires confirmation | 2,075 zeros; IQR flags: 305 | What counts as organic and how does it relate to paid Channel0? |
| `Promo` | decimal | Promotion or commercial-event covariate | Field labelled `Promo` | Unknown — requires confirmation | Minimum 0; maximum 4.800555; 248 IQR flags | Is it an intensity, indicator, index, or amount? |
| `conversions` | decimal | Primary candidate outcome | Field labelled conversions | Unknown — requires confirmation | No negative values; mean 10,565,819.57; 56 IQR flags | Are these transactions, leads, attributed conversions, or a simulated rate? |
| `revenue_per_conversion` | decimal | Revenue KPI or outcome-side covariate | Field labelled revenue per conversion | Unknown — requires confirmation | Mean about 0.020002; 43 IQR flags | Currency, ratio, simulated index, and whether it is measured independently of conversions? |
| `population` | decimal | Market-size control / denominator | Field labelled population | Unknown — requires confirmation | No negative values; no IQR flags; mean 542,418.83 | Is it static or time-varying population, and for what geography/date? |

### 3.1 Confirmed facts versus reasonable interpretations

**Confirmed by the repository and observed data:**

- The dataset is simulated marketing-mix data.
- The row key is unique `geo` plus `time`.
- Five paid channels have paired impression and spend fields.
- The raw file contains fields labelled controls, conversions, promotion,
  revenue per conversion, and population.
- Paid spend and impression zero states match for all five channels.
- The raw file contains no missing cells or mechanically invalid dates.

**Reasonable analytical interpretations, not confirmed business facts:**

- Spend and impressions are candidate paid-media exposures.
- `conversions` is a candidate target.
- `population` may help separate market size from performance.
- `Promo`, competitor sales, and sentiment may be confounders or controls.
- `geo` may require fixed effects or hierarchical treatment.

**Unknown and requiring confirmation:**

- Units, currencies, denominators, attribution windows, and operational
  definitions for all measures.
- Whether a field is generated independently, contemporaneously, or with
  lagged relationships.
- Whether the simulated data is intended to reproduce a particular causal
  data-generating process.

## 4. Important data-handling decisions

### 4.1 Exported index: `Unnamed: 0`

`Unnamed: 0` is an exact zero-based sequence aligned with row order. This is
consistent with an index written to CSV without a column name, not a business
measure. It contains no geography, time, activity, or outcome information
that should be learned by a model.

**Recommendation:**

1. Preserve it in the immutable raw file.
2. Exclude it from modelling features and database facts.
3. If row lineage is needed, retain it as a technical ingestion identifier
   outside the feature set.
4. Record the exclusion in the preparation metadata and dataset version.

Dropping it from a derived modelling table is safe after the raw-file
preservation and lineage policy are in place. It should not be used as a
predictor because a model could learn file ordering rather than business
signal.

### 4.2 Zero-heavy marketing channels

The validator found the following zero-spend counts:

| Channel | Zero spend rows | Share of 6,240 | Zero impression rows | Spend/impression zero mismatch |
|---|---:|---:|---:|---:|
| Channel0 | 755 | 12.10% | 755 | 0 |
| Channel1 | 1,742 | 27.92% | 1,742 | 0 |
| Channel2 | 4,010 | 64.26% | 4,010 | 0 |
| Channel3 | 169 | 2.71% | 169 | 0 |
| Channel4 | 820 | 13.14% | 820 | 0 |

The matching zero states support the interpretation that these are inactive
or no-activity observations rather than missing values. They do not prove why
activity is zero. It could reflect campaign scheduling, channel availability,
targeting, or a simulated design.

**Decision now:** keep zero values as zero. Do not convert them to `NULL`,
impute them, or remove their rows.

**Later analytical implications:**

- Log transforms require a documented zero strategy, such as a
  pre-specified offset, and must not silently transform zero into an
  arbitrary positive exposure.
- MMM adstock and saturation functions must define their zero behaviour.
- A high zero rate can make a channel's response hard to identify and can
  produce unstable coefficients if active observations are limited or
  correlated with geography and time.
- A two-part diagnostic may be useful later: probability of activity and
  level conditional on activity. This is a modelling option, not a current
  data-cleaning rule.
- Zero observations should remain available for counterfactual and inactive
  period comparisons, subject to causal-design assumptions.

### 4.3 Negative control variables

`competitor_sales_control` is negative in 3,238 rows and
`sentiment_score_control` is negative in 3,216 rows. The repository does not
document their baselines, ranges, transformations, or units.

Negative values may be valid for centred scores, changes, anomalies, or
indices. They may also indicate a semantic or ingestion problem. Magnitude
alone cannot distinguish these possibilities.

**Decision now:** retain the values unchanged and do not apply absolute value,
clipping, shifting, or sign reversal.

Before preprocessing, obtain:

- Definition and source of each control
- Original scale and valid range
- Baseline and interpretation of zero
- Whether values are levels, changes, z-scores, or indices
- Timing and geography alignment
- Whether the control is known before the outcome period

Only then should a transformation, standardisation, lag, or missingness rule
be selected.

### 4.4 Outliers

The existing IQR screen identifies values outside
`Q1 - 1.5 × IQR` or `Q3 + 1.5 × IQR`. It is a distributional screening
device, not a truth detector. It is especially sensitive to the
zero-inflated, right-skewed channel distributions.

Flags include:

- Channel2 spend and impressions: 941 each
- Channel0 spend and impressions: 164 each
- Channel1 spend and impressions: 215 each
- Channel3 spend and impressions: 108 each
- Channel4 spend and impressions: 143 each
- Organic impressions: 305
- `Promo`: 248
- `conversions`: 56
- `revenue_per_conversion`: 43
- Each negative-valued control: 61
- `population`: 0

**Decision now:** do not delete, cap, winsorise, or replace these observations.
An unusually large campaign or conversion week can be genuine and may be
important for estimating response. Removing it can bias channel contribution
and understate real-world variance.

Useful follow-up investigation:

- Check flagged rows against source or campaign metadata.
- Examine whether flags cluster in specific geographies or dates.
- Compare paired spend and impression relationships.
- Check whether values are within documented operational limits.
- Run sensitivity analyses with and without flagged observations only after
  the modelling protocol defines the comparison.

## 5. Geography and population considerations

All 40 geographies have 156 weekly observations. EDA shows substantial
geography-level differences in mean conversions; the highest and lowest
geographies differ materially. Population also varies widely, with an observed
mean of approximately 542,419 and standard deviation of approximately 242,840.

Large geographies can naturally have more conversions, impressions, and spend
without having better channel efficiency. Therefore:

- Absolute conversions answer a scale question.
- Conversions per population answer a size-normalised descriptive question.
- Neither alone establishes incremental channel contribution.
- Dividing by population can introduce its own interpretation and noise if
  population is not the correct exposure denominator.

Potential future approaches include geography fixed effects, hierarchical
effects, population as a covariate, or carefully justified rate/offset
specifications. The choice depends on the confirmed outcome definition and
whether population is static, time-varying, pre-treatment, and measured at
the same geography level.

The data supports geography-aware exploration now. It does not support a
causal claim that high-spend or high-conversion geographies are more efficient.
The existing raw correlations are associations and may reflect market size,
targeting, seasonality, geography effects, or other controls.

## 6. Weekly time structure and forecasting limitations

The date field has 156 unique dates at seven-day intervals from 2021-01-25 to
2024-01-15. The last calendar year is partial: only three observations are
present in 2024. The data therefore covers multiple full years but does not
provide a complete 2024 annual period.

Potential temporal concerns:

- Seasonal effects may exist but have not been formally tested.
- Marketing effects may be delayed; same-week spend may not capture lagged
  response.
- Weekly observations are serially dependent within a geography.
- Common time shocks can affect all geographies.
- Campaign schedules and promotions may be seasonal or event-driven.
- A random row split can place future information in training data and break
  temporal ordering.
- The short 2024 tail limits robust full-year holdout evaluation.

For forecasting or time-dependent modelling, chronological validation is more
appropriate: train on earlier weeks and evaluate on later weeks. Candidate
backtests should be defined by date, keep all geographies aligned within each
period, and document the horizon. Random train-test splitting should not be
used as the primary forecasting validation design.

## 7. Modelling-readiness assessment

“Ready” below means ready for the narrowly described analytical activity, not
proof that the dataset supports causal conclusions.

| Analytical task | Required inputs | Current readiness | Missing information | Recommended next action |
|---|---|---|---|---|
| Descriptive marketing performance analysis | Valid rows, geography, dates, activity and outcome labels | **Ready for exploration** | Units and business definitions limit interpretation | Produce geography, time, activity, and zero-state summaries with explicit caveats |
| Channel performance comparison | Comparable spend/impression definitions, outcome definition, geography and time context | **Conditionally ready** | Currency, attribution windows, outcome definition, market-size treatment | Confirm units and compare within geography/time; avoid ranking as ROI |
| Regression analysis | Defined target, valid predictors, leakage policy, geography/time controls | **Conditionally ready** | Control semantics, target definition, temporal ordering, functional forms | Write a model specification and leakage review before fitting models |
| Marketing Mix Modelling | Outcome, spend units, channel mappings, lag/adstock assumptions, sufficient variation, validation design | **Requires business confirmation** | All major semantic and attribution assumptions remain open | Confirm data-generating definitions, then design geo-week MMM and diagnostics |
| Time-series forecasting | Defined target, date convention, forecast horizon, history, exogenous-variable availability | **Conditionally ready** | Partial 2024, target meaning, future availability of controls, seasonality and lag policy | Use chronological backtesting and define an explicit forecast horizon |
| Budget allocation and optimisation | Validated causal or decision model, budget constraints, response curves, objective and guardrails | **Not ready** | No validated response model, ROI units, budget constraints, or business objective | Defer until MMM/response estimates and decision constraints are validated |

No positive spend-conversion correlation should be interpreted as causal
incrementality, ROI, or a recommendation to increase spend.

## 8. Preliminary preprocessing specification

This is a design specification only. It does not implement transformations.

| Proposed step | Columns affected | Why needed | Safe now? | Business confirmation needed? | Preservation / reproducibility |
|---|---|---|---|---|---|
| Read raw CSV as immutable input | All | Establish a stable source | Yes | No | Keep the raw file unchanged; record source hash/version in a future pipeline |
| Validate schema and types | All | Catch structural drift before use | Yes | No | Reuse `src/validation.py`; save validation output with the derived dataset |
| Parse `time` into a typed weekly date | `time` | Enable ordering, joins, lags, and date dimensions | Yes, as a derived field | Confirm week-label convention | Preserve original string and retain parsed field in derived data |
| Exclude `Unnamed: 0` from features | `Unnamed: 0` | Prevent row-order leakage and meaningless predictor use | Yes | Confirm lineage requirements | Retain only in raw/technical lineage metadata |
| Keep `geo` as a stable identifier | `geo` | Preserve panel structure and geography effects | Yes | Confirm entity meaning | Use a deterministic geography key mapping; never overwrite raw labels |
| Keep legitimate zero activity as zero | Paid spend/impressions, organic impressions | Preserve inactive periods and avoid invented exposure | Yes | Confirm zero semantics if possible | Add no imputation; document zero counts and transformation rules |
| Investigate control scales before transformation | Two control fields | Negative values may be valid or erroneous | No transformation yet | Yes | Preserve original columns; version any later transform and rationale |
| Investigate outliers without deletion | All numeric fields | Separate unusual from erroneous observations | Screening is safe; treatment is not | Yes, using source/campaign context | Store flags separately; preserve original values |
| Evaluate population normalisation | `population`, `conversions`, activity fields | Separate market size from rates where appropriate | Diagnostic ratios only | Yes; confirm denominator and timing | Keep absolute and derived measures distinct |
| Define target and leakage policy | `conversions`, revenue field, controls, future activity | Prevent post-outcome or future information leakage | No target choice yet | Yes | Record feature availability time and target window |
| Design channel transformations | Spend/impression fields | MMM may need lag, saturation, or exposure choice | No | Yes; channel and attribution confirmation | Use deterministic, parameter-versioned transformations |
| Create modelling split by date | `time`, `geo` | Respect temporal dependence | Yes for design | Confirm forecast horizon | Store cutoff dates and evaluation windows |

### 8.1 Candidate derived modelling fields

Potential derived fields include a parsed date, calendar year/week,
geography key, channel activity indicators, population-normalised descriptive
metrics, and lagged/adstocked media variables. None should replace the raw
fields. In particular:

- An activity indicator may be useful for diagnosing zero inflation, but does
  not prove a two-part model is appropriate.
- A log-spend field needs an explicit zero policy and should not be created
  silently.
- A per-capita conversion metric is descriptive until the correct population
  denominator and timing are confirmed.
- Adstock and saturation parameters must be part of a versioned model
  specification, not an untracked cleaning operation.

## 9. Preliminary MySQL 8.x database architecture

The database technology is assumed to be MySQL 8.x for this design exercise.
No database objects are created here.

### 9.1 Wide versus long storage

| Criterion | Wide format: one geo-week row | Long format: one geo-week-channel row |
|---|---|---|
| Data redundancy | Geography/date repeated once; channel columns grow horizontally | Geography/date repeated per channel, but channel attributes are normalised |
| Query simplicity | Simple for current five-channel extracts and direct feature matrices | Simple for channel filters, aggregation, and scalable channel queries |
| Channel scalability | Requires schema changes for each new channel | Add a channel dimension row and fact rows |
| ETL complexity | Straightforward load from current CSV | Requires unpivoting the current file |
| Analytical SQL | Convenient for fixed-channel wide regressions | More natural for channel summaries and dynamic channel sets |
| MMM preparation | Convenient for matrix-shaped model inputs | Requires pivoting or conditional aggregation before some models |
| Data quality constraints | Paired fields and channel rules are repeated in columns | Channel-level keys and constraints can be applied consistently |

### 9.2 Recommendation: hybrid architecture

Use a **long channel fact model as the canonical analytical storage**, with a
derived wide modelling view or export for algorithms that require one row per
geo-week and one feature per channel.

Reasons:

1. New channels can be added without adding columns to the fact table.
2. Channel metadata, naming, and status can be managed centrally.
3. Channel-level SQL is simpler for spend, impressions, zero-state, and
   aggregation queries.
4. A wide view preserves convenient MMM matrix preparation without making the
   database schema channel-specific.
5. The raw CSV can be loaded into a staging area first, then validated and
   transformed into governed dimensions and facts.

The canonical database should still preserve a source-row lineage reference
and validation status. The exported index should not become an analytical
measure.

### 9.3 Conceptual dimensions and fact

#### `dim_geography`

Conceptual attributes:

- `geography_key`: surrogate key
- `geo_code`: original `geo` value, unique
- Geography name/type: only when confirmed
- Population attributes: only if their temporal grain and definition are
  confirmed
- Source and effective-date metadata if geography definitions can change

The original `geo` label should be retained. Do not invent geography names or
hierarchies.

#### `dim_date`

Conceptual attributes:

- `date_key`: surrogate or deterministic date key
- `week_start_date` or source date label, after confirming convention
- Calendar year
- Week number
- Month/quarter
- Fiscal attributes only if the business calendar is confirmed

The current data supports a weekly date dimension, but the meaning of the
source date label must be documented first.

#### `dim_channel`

Conceptual attributes:

- `channel_key`
- `channel_code` such as `Channel0`
- Display name and channel type, only when confirmed
- Paid/organic classification
- Spend and impression definition metadata
- Effective dates for channel mapping changes

The current file's generic channel names should remain generic until
provenance confirms their real-world mapping.

#### `fact_marketing_performance`

At the recommended long grain, one row represents one
geography-week-channel observation. Conceptual measures and keys:

- `geography_key`
- `date_key`
- `channel_key`
- Source lineage identifier
- Spend measure
- Impression measure
- Activity-state indicator, if defined as a derived diagnostic
- Validation/status metadata

Geo-week measures not naturally channel-specific should be stored separately
or in a geo-week fact, depending on confirmed warehouse requirements:

- `conversions`
- `revenue_per_conversion`
- `Promo`
- `competitor_sales_control`
- `sentiment_score_control`
- `population`

Duplicating geo-week outcomes across channel rows is possible but introduces
aggregation risk. A separate `fact_geo_week_outcome` or a governed wide view
would avoid double-counting. The final choice depends on the intended
reporting queries, but the grain must be explicit in every table and view.

## 10. Unresolved business questions

Before causal or decision modelling, obtain answers to:

1. What does each generic channel represent?
2. What currency and time window do spend values use?
3. What type of impressions are recorded, and are they comparable across
   channels?
4. What exactly is a conversion, and is it a count, rate, or modelled value?
5. What does `revenue_per_conversion` measure, and is it independent of the
   target?
6. What is the scale and valid range of `Promo`?
7. Why can both control variables be negative?
8. What are the sources, timestamps, and geographic alignment of the controls?
9. Does `population` vary by week, and what population definition is used?
10. Is `Organic_channel0_impression` measured with the same geography and
    weekly window as paid activity?
11. Does `time` represent week start, week end, or another reporting date?
12. Are there known campaign lags, attribution windows, or media carryover
    effects?
13. Are future control values available at forecast time?
14. What decision objective, budget constraints, and guardrails would an
    eventual optimiser need?
15. Is the simulated data intended for methodological demonstration rather
    than operational business decisions?

## 11. Recommended next development milestone

The next milestone should be **confirmed modelling-input design and a
versioned preparation-data plan**, not model fitting.

Recommended deliverables:

1. A source glossary confirming variable meanings, units, timing, and
   geography definitions.
2. A written target and leakage policy.
3. A documented policy for zero-heavy media, controls, and outlier review.
4. A chronological train/validation/test design for any forecasting task.
5. A deterministic derived-data specification that preserves raw lineage.
6. A decision on the canonical MySQL fact grain and the wide modelling view.
7. Tests for the future preparation pipeline before any MMM or forecasting
   implementation.

Only after these decisions are confirmed should MarketMosaic proceed to data
preparation and then a separately validated MMM or forecasting milestone.

## 12. Current conclusion

The dataset is structurally reliable and useful for exploration. It is not
fully modelling-ready in the business or causal sense. The correct engineering
position is:

- **Use now:** validated descriptive analysis and schema/lineage design.
- **Use conditionally:** regression and forecasting prototypes with explicit
  caveats, chronology, and sensitivity analysis.
- **Do not use yet:** ROI claims, causal channel contribution, budget
  optimisation, or production decisions.

All recommendations preserve the raw CSV, avoid invented semantics, retain
legitimate zero observations, and defer irreversible transformations until
their business rationale is confirmed.
