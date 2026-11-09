# MarketMosaic Daily Work Report — 2026-11-07

## Project objective and today's milestone

MarketMosaic is an end-to-end marketing analytics and decision science project
for understanding marketing performance, validating multi-channel data,
building future modelling inputs, and eventually supporting forecasting and
budget decisions.

Today's milestone was to establish a reliable data foundation through:

- Reusable data validation checks
- Automated tests for validation and existing functionality
- A data validation report
- A data dictionary
- Verification of the raw simulated marketing-mix dataset

The raw dataset was preserved, and no modelling, ETL, database, optimization,
dashboard, or deployment work was started.

## Files created and modified

### Created

- `src/validation.py`
  - Reusable validation functions and validation report generation.
- `tests/test_validation.py`
  - Synthetic edge-case tests and a real-dataset validation smoke test.
- `reports/data_validation.md`
  - Dataset validation results, handling decisions, and readiness assessment.
- `reports/data_dictionary.md`
  - Column-level observed types, known meanings, and unresolved units.
- `reports/2026-11-07_work_report.md`
  - This daily work report.

### Modified

- `src/eda.py`
  - Integrated the reusable validator into `data_quality_report()`.

### Not modified

- `data/raw/geo_all_channels.csv`
- `notebooks/eda_week1.ipynb`
- Existing EDA and inspection test files
- Existing figures and unrelated project files

## Technical implementation details

`src/validation.py` provides explicit, reusable checks for:

- Expected and unexpected columns
- Numeric, categorical, and date data types
- Missing cells
- Exact duplicate rows
- Duplicate `geo`/`time` keys
- Invalid or unparseable dates
- Weekly date continuity and unexpected gaps
- Geography coverage and balanced geography-week panel consistency
- Negative values in fields where non-negativity is unambiguous
- Spend/impression zero-state mismatches
- Exported `Unnamed: 0` index handling
- IQR-based outlier screening

Validation returns structured results without modifying the input DataFrame.
An optional `raise_on_error=True` mode raises a clear `ValidationError` when
structural validation fails.

Zero activity is reported rather than rejected. Outliers are flagged for
investigation rather than removed. The raw CSV remains unchanged.

The existing `data_quality_report()` function in `src/eda.py` now includes the
reusable validation output while preserving its prior summary fields.

## Dataset validation results

The actual raw dataset contains:

- 6,240 rows
- 20 raw columns
- 40 geographies
- 156 weekly periods
- Date range: 2021-01-25 through 2024-01-15
- Balanced panel: 40 geographies × 156 periods

Mechanical validation results:

- Missing required columns: 0
- Unexpected columns: 0
- Invalid observed data types: 0
- Missing cells: 0
- Exact duplicate rows: 0
- Duplicate geography-week keys: 0
- Invalid dates: 0
- Unexpected weekly gaps: 0
- Incomplete geography panels: 0
- Incomplete date coverage: 0
- Negative values in enforced non-negative fields: 0
- Spend/impression zero-state mismatches: 0
- Exported index check: passed; values form the sequence 0–6,239

Zero activity is present and was retained:

- Channel0: 755 zero-spend rows
- Channel1: 1,742 zero-spend rows
- Channel2: 4,010 zero-spend rows
- Channel3: 169 zero-spend rows
- Channel4: 820 zero-spend rows

The two control variables contain negative values:

- `competitor_sales_control`: 3,238 negative rows
- `sentiment_score_control`: 3,216 negative rows

These were not classified as invalid because their scales and baselines have
not been established.

The IQR screen flagged potential outliers, including 941 rows for Channel2
spend/impressions, 56 conversion rows, 43
`revenue_per_conversion` rows, 248 `Promo` rows, and additional flags in
other activity and control fields. No observations were deleted.

## Test execution results

The full test suite was executed from the project root:

```text
31 passed, 4 warnings
```

The passing suite included:

- Existing EDA tests
- Existing data inspection tests
- Validation tests using small synthetic DataFrames
- Validation of the actual raw dataset
- Tests for missing columns, invalid types, missing values, duplicates,
  duplicate keys, invalid dates, missing weeks, negative values, zero
  activity, outlier preservation, and exported index handling

The four warnings were existing pandas compatibility/runtime warnings emitted
by `inspect_data.py`; they did not cause test failures.

## Issues and unresolved assumptions

The dataset is mechanically clean, but the following still require
confirmation before business interpretation or production modelling:

- Currency and units for channel spend
- Units for impressions
- Exact definition and unit of conversions
- Meaning and unit of `revenue_per_conversion`
- Meaning and scale of `Promo`
- Whether negative control values are expected because the controls are
  centred, indexed, or otherwise transformed
- Meaning and unit of `Organic_channel0_impression`
- Weekly calendar convention
- Business meaning of the geography identifiers

`Unnamed: 0` is an exported row index rather than a business measure and
should not be used as a model feature.

## Engineering decisions and data-handling choices

- Extended the existing EDA quality workflow instead of creating a duplicate
  quality implementation.
- Kept validation rules explicit and modular.
- Preserved the original raw dataset.
- Did not silently drop rows or impute values.
- Did not treat every zero as invalid.
- Did not automatically remove outliers.
- Did not invent variable units or business definitions.
- Applied non-negativity checks only where the requirement is logically clear.
- Reported definition-dependent negative control values as an assumption to
  confirm.
- Used small synthetic DataFrames for validation edge-case tests.
- Kept the scope limited to data validation, testing, and documentation.

## Current project completion status

Today's data foundation milestone is **complete**. The project now has
validated raw-data checks, automated coverage for the validation behavior,
documented dataset results, and a column-level data dictionary.

The dataset is ready as a validated raw analytical input. It is not yet ready
for causal interpretation or production modelling until the outstanding
semantics and units are confirmed.

## Next milestone and roadmap

The next logical milestone is to create a modelling-preparation
specification. It should confirm variable semantics and units and define the
handling of:

1. The exported index column
2. Zero-heavy channels, especially Channel2
3. Negative-valued control variables
4. Potential outlier review
5. Geography and population effects
6. Weekly time representation

After that specification is confirmed, the roadmap can proceed to controlled
data preparation and later milestones: ETL/database work, Marketing Mix
Modelling, forecasting, budget optimization, dashboards, and deployment.
