# MarketMosaic Week 1 EDA and Data Audit

**Status:** Complete for the Week 1 inspection/EDA milestone  
**Dataset:** `data/raw/geo_all_channels.csv` (simulated Google Meridian marketing-mix data)  
**Notebook:** [`notebooks/eda_week1.ipynb`](../notebooks/eda_week1.ipynb)  
**Reusable implementation:** [`src/eda.py`](../src/eda.py)  
**Figures:** `reports/figures/` after running the notebook

All numerical claims below were calculated from the CSV on November 5, 2026. A correlation is an association, not proof that changing spend caused conversions.

## What We Discovered From The Data

### 1. Dataset overview

This is a **simulated marketing-mix panel**. A panel combines repeated observations across entities: here, each row represents one geography (`geo`) in one weekly period (`time`). There are **6,240 rows**, **20 raw columns**, **40 geographies**, and **156 weekly time periods**, covering **2021-01-25 through 2024-01-15**. Every geography has 156 rows, so the panel is balanced.

The columns fall into these groups:

* **Identity/time:** `geo`, `time`, plus `Unnamed: 0`, which is a sequential exported row number rather than a business measure.
* **Paid media activity:** five channel pairs, `Channel0` through `Channel4`, each with impressions and spend.
* **Controls:** `competitor_sales_control`, `sentiment_score_control`, and `Promo`. These represent non-channel context that may also affect the outcome.
* **Outcome/financial variables:** `conversions` and `revenue_per_conversion`.
* **Market context:** `population`, which indicates the size of the geography.
* **Organic activity:** `Organic_channel0_impression`.

The raw dataset has 18 numerical columns and two text columns (`geo`, `time`). The notebook adds `time_dt` as a parsed datetime helper; it does not alter the raw CSV.

### 2. Statistical findings

The complete table is generated in notebook section **3. Statistical findings** with `descriptive_statistics()`. Selected verified values are:

| Variable | Mean | Median | Standard deviation | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|
| Channel0 spend | 6,490.66 | 4,983.84 | 6,008.03 | 0 | 38,071.73 |
| Channel1 spend | 5,019.28 | 2,995.07 | 5,983.57 | 0 | 42,397.70 |
| Channel2 spend | 1,935.79 | 0 | 4,125.53 | 0 | 41,688.65 |
| Channel3 spend | 14,080.19 | 11,731.18 | 10,168.24 | 0 | 59,499.48 |
| Channel4 spend | 7,649.15 | 5,814.69 | 7,123.18 | 0 | 54,352.81 |
| Conversions | 10,565,819.57 | 9,709,094.50 | 6,079,410.89 | 484,031.22 | 36,712,692.00 |
| Revenue per conversion | 0.020002 | 0.020003 | 0.000099 | 0.019650 | 0.020363 |
| Promo | 0.492528 | 0.084382 | 0.694279 | 0 | 4.800555 |
| Population | 542,418.83 | 560,478.83 | 242,839.72 | 136,670.94 | 994,048.94 |

The spend means being larger than the medians, especially for Channel2, indicate right-skew: many rows have low/zero spend while a smaller number have large campaigns. Channel2 is especially sparse: **4,010 of 6,240 rows (64.26%)** have zero spend/impressions. Zero activity is also present in Channel1 (1,742 rows), Channel4 (820), Channel0 (755), and Channel3 (169).

Conversions vary substantially: the standard deviation is about 6.08 million versus a mean of 10.57 million. Revenue per conversion is comparatively stable around 0.02. An IQR screen flagged 56 conversion rows, 164 Channel0-spend rows, 215 Channel1 rows, 941 Channel2 rows, 108 Channel3 rows, 143 Channel4 rows, 43 revenue-per-conversion rows, 248 Promo rows, and 61 rows each for the two controls. These are **screening flags**, not proof of bad data; zero-heavy channel distributions make IQR fences particularly sensitive.

### 3. Channel-level findings

| Channel | Mean spend | Total spend | Mean impressions | Total impressions | Zero rows | Spend/conversions correlation |
|---|---:|---:|---:|---:|---:|---:|
| Channel0 | 6,490.66 | 40,501,713.08 | 885,163.54 | 5,523,420,467 | 755 | 0.4138 |
| Channel1 | 5,019.28 | 31,320,298.20 | 520,605.54 | 3,248,578,573 | 1,742 | 0.2931 |
| Channel2 | 1,935.79 | 12,079,349.34 | 260,505.03 | 1,625,551,369 | 4,010 | 0.1479 |
| Channel3 | 14,080.19 | 87,860,358.25 | 1,806,810.45 | 11,274,497,204 | 169 | 0.4689 |
| Channel4 | 7,649.15 | 47,730,683.48 | 981,677.97 | 6,125,670,562 | 820 | 0.3482 |

Channel3 is the largest channel by both spend and impressions. Channel2 is the smallest and most frequently inactive. The positive correlations mean rows with more activity tend to have more conversions in this raw comparison. Channel3 has the strongest observed linear association (0.4689), followed by Channel0 (0.4138); Channel2 is weakest (0.1479). This does **not** establish ROI or causal effectiveness because geography size, time, controls, targeting, and the other channels are not held constant.

Spend correlations range from 0.3036 to 0.6301. The strongest pair is Channel3 and Channel4 (0.6301), followed by Channel3/Channel0 (0.5324) and Channel3/Channel2 (0.5236). This is meaningful for MMM: coefficients may become unstable if channels move together, so regularisation, diagnostics, and careful feature design will be needed.

### 4. Geographical findings

All 40 geographies have 156 observations. Highest mean conversions are:

* **Geo36:** 21,093,364.53 mean conversions; population 969,886.50; total spend 9,761,024.15.
* **Geo39:** 20,659,273.94; population 798,939.10; total spend 7,801,774.61.
* **Geo10:** 19,833,038.62; population 994,048.94; total spend 9,680,096.29.
* **Geo23:** 18,182,370.63; population 981,570.90; total spend 9,937,169.58.
* **Geo31:** 17,209,421.54; population 873,369.70; total spend 8,667,994.60.

Lowest mean conversions are Geo0 (2,313,344.05), Geo24 (2,560,902.94), Geo1 (3,341,781.85), Geo3 (4,152,411.80), and Geo6 (4,155,831.97). The range between Geo0 and Geo36 is large, so geography effects are not optional modelling details. Spend is also higher in large/high-conversion geographies, but this comparison is descriptive and population is a likely confounder. The geography chart in notebook section **6. Visualisations** makes the full ranking visible.

### 5. Temporal findings

The data contains 156 weekly dates. Mean conversions by year were 10,385,944.75 (2021), 10,641,290.98 (2022), 10,664,418.40 (2023), and 10,486,557.40 (2024; only three weeks). The first period's total conversions were 386,300,926.30 and the final period's were 422,429,715.80. The highest total-conversion week was 2023-05-15 (491,287,369.30); the lowest was 2022-09-19 (340,283,293.30).

The year means do not show a simple monotonic trend. The short 2024 segment must not be interpreted as a full-year trend. Weekly variation is visible in the trend chart, but this EDA does not claim a confirmed seasonal effect: formal seasonality testing/decomposition remains a modelling task.

### 6. Data quality findings

Verified checks:

* Missing cells: **0**.
* Exact duplicate rows: **0**.
* Duplicate `geo + time` keys: **0**; this combination is unique.
* Invalid parsed dates: **0**.
* `Unnamed: 0` has 6,240 unique values from 0 to 6,239 and exactly equals a zero-based sequence. It is an index artifact and should normally be dropped before modelling, not treated as a predictor.
* The panel is balanced: 40 geographies × 156 periods = 6,240 rows.

The dataset is clean in the mechanical sense, but “no missing values” does not guarantee semantic correctness. Units, channel names, simulated-generation assumptions, and the meaning of controls should be documented before causal interpretation.

### 7. Implications for MarketMosaic

The dataset is suitable for the next modelling stage after explicit preparation:

1. Parse and validate `time`, drop `Unnamed: 0`, and preserve `geo` as a panel identifier.
2. Keep geography and population in the model so large markets are not confused with more efficient media.
3. Consider channel sparsity and skew. Channel2's 64.26% zero rate may require a deliberate transformation or a model that handles intermittent activity.
4. Investigate multicollinearity. The maximum pairwise channel-spend correlation is 0.6301, not automatically disqualifying but high enough to monitor with VIF, coefficient stability, and out-of-sample validation.
5. Do not convert the raw correlations into ROI. MMM needs lag/adstock, saturation, controls, time effects, geography effects, and validation before budget decisions.
6. Investigate the flagged outliers and the units of `revenue_per_conversion` before interpreting financial results.

### 8. Explanation of every visualisation

1. **`01_distributions.png` — distributions of conversions and spend.** Created to see typical values, skew, zeros, and extreme observations. The conversions histogram is broad, while spend boxplots show different channel scales and many zero/low observations, especially Channel2. It supports using robust summaries and transformations; it does not by itself identify bad records.
2. **`02_channel_spend_comparison.png` — total spend by channel.** Created to compare aggregate budget scale. Channel3 is highest and Channel2 lowest. It describes allocation, not efficiency, because it does not divide by conversions or control for confounders.
3. **`03_spend_vs_conversions.png` — five scatterplots.** Each point is a geography-week record; the x-axis is one channel's spend and y-axis is conversions. Positive but dispersed clouds match the correlations above. The plot supports association, not causal lift.
4. **`04_geography_conversions.png` — mean conversions by geography.** Created to expose heterogeneity across markets. Geo36 and Geo39 are near the top; Geo0, Geo24, and Geo1 are near the bottom. Population and other context mean the chart is not a fairness or ROI ranking.
5. **`05_weekly_conversions.png` — weekly total conversions.** Created to reveal time variation, spikes, dips, and possible seasonality. It shows meaningful week-to-week movement and no simple linear trend. Formal decomposition is intentionally deferred.

### 9. Implementation walkthrough

The notebook runs top-to-bottom:

1. Imports pandas, seaborn, matplotlib, pathlib, and the reusable functions.
2. Locates the project root and loads the CSV through `load_and_prepare_data()`.
3. Parses `time` with `pd.to_datetime(..., errors="coerce")`; invalid dates become detectable nulls rather than silently remaining strings.
4. Prints shape, geography count, period count, date range, and dtypes.
5. Runs `data_quality_report()`, which uses `isna().sum()`, `duplicated()`, `groupby()`, `nunique()`, and a comparison with `range(len(data))`.
6. Runs `descriptive_statistics()`, a thin wrapper around `DataFrame.describe().T`.
7. Builds channel summaries with a loop over the five paired column names, computing means, medians, totals, zero counts, and Pearson `.corr()`.
8. Aggregates geography and week tables using `groupby().agg()` and adds total spend across the five spend columns.
9. Creates five saved figures with seaborn/matplotlib. `melt()` converts wide spend columns into a long plotting table for the boxplot.

Technically, the important lesson is separation of concerns: loading/validation, summary calculations, aggregation, and visualisation are reusable functions in [`src/eda.py`](../src/eda.py), while the notebook is the readable execution narrative. The tests verify shape, quality checks, panel dimensions, channel labels, and correlation output.

### 10. Final milestone report

**Completed tasks**

* Confirmed the raw dataset and its panel structure.
* Added reusable EDA functions for preparation, descriptive statistics, quality, channel, geography, time, correlations, and figures.
* Added `notebooks/eda_week1.ipynb` with beginner-friendly sections.
* Added automated tests for the real dataset and EDA outputs.
* Replaced placeholder audit values with calculated numerical evidence.

**Tests and execution results**

Run from the project root:

```text
pytest
```

The targeted EDA and existing inspection tests should pass. The notebook is designed to run in order; its final cell saves the five PNG figures to `reports/figures`.

**Files created or modified**

* Created [`src/eda.py`](../src/eda.py)
* Created [`tests/test_eda.py`](../tests/test_eda.py)
* Created [`notebooks/eda_week1.ipynb`](../notebooks/eda_week1.ipynb)
* Replaced [`reports/data_audit.md`](data_audit.md)

**Remaining tasks**

* Confirm the semantic meaning and units of every simulated variable.
* Decide transformations/adstock/saturation and treatment of zero-heavy channels.
* Add formal seasonality/time-series diagnostics.
* Build and validate the first MMM, including out-of-sample checks and multicollinearity diagnostics.
* Add model-specific ROI and budget optimisation only after the model is validated.

**Is Week 1 genuinely complete?** Yes, for the project blueprint's **Project Setup & Data Inspection** milestone plus the requested EDA deliverable: the data has been inspected, quality-tested, statistically summarised, compared by channel/geography/time, visualised, documented, and covered by tests. Week 2 (preprocessing and the first formal MMM) is not complete and should not be claimed as complete.
