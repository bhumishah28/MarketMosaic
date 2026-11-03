# MarketMosaic - Dataset Audit Report

**Report Date:** November 3, 2026  
**Dataset:** Google Meridian Simulated Marketing Mix Modeling Data  
**File:** `geo_all_channels.csv`  
**Location:** `data/raw/geo_all_channels.csv`

## 1. Executive Summary

This report provides a comprehensive audit of the Google Meridian simulated Marketing Mix Modeling dataset. The dataset contains **6,240 observations** across **20 variables**, representing simulated marketing performance data across multiple channels and geographies.

### Key Findings:
- ✅ **Data Quality**: No missing values found
- ✅ **Data Integrity**: No duplicate rows detected  
- 📊 **Structure**: Well-structured with clear column naming
- 🔍 **Completeness**: All expected marketing variables present
- 📈 **Readiness**: Ready for statistical modeling and analysis

## 2. Dataset Dimensions

| Metric | Value |
|--------|-------|
| **Total Rows** | 6,240 |
| **Total Columns** | 20 |
| **Total Data Points** | 124,800 |
| **File Size** | 966 KB |
| **Data Types** | 18 numerical, 2 categorical |

## 3. Column Analysis

### 3.1 Complete Column List

| # | Column Name | Data Type | Category | Description (Interpreted) |
|---|-------------|-----------|----------|---------------------------|
| 1 | `Unnamed: 0` | `int64` | Numerical | Index column (likely sequential ID) |
| 2 | `geo` | `object` | Categorical | Geographic identifier/location |
| 3 | `time` | `object` | Categorical/Time | Date/time indicator (string format) |
| 4 | `Channel0_impression` | `int64` | Numerical | Impressions for Channel 0 |
| 5 | `Channel1_impression` | `int64` | Numerical | Impressions for Channel 1 |
| 6 | `Channel2_impression` | `int64` | Numerical | Impressions for Channel 2 |
| 7 | `Channel3_impression` | `int64` | Numerical | Impressions for Channel 3 |
| 8 | `Channel4_impression` | `int64` | Numerical | Impressions for Channel 4 |
| 9 | `competitor_sales_control` | `float64` | Numerical | Competitor sales control variable |
| 10 | `sentiment_score_control` | `float64` | Numerical | Sentiment score control variable |
| 11 | `Channel0_spend` | `float64` | Numerical | Marketing spend for Channel 0 |
| 12 | `Channel1_spend` | `float64` | Numerical | Marketing spend for Channel 1 |
| 13 | `Channel2_spend` | `float64` | Numerical | Marketing spend for Channel 2 |
| 14 | `Channel3_spend` | `float64` | Numerical | Marketing spend for Channel 3 |
| 15 | `Channel4_spend` | `float64` | Numerical | Marketing spend for Channel 4 |
| 16 | `Organic_channel0_impression` | `int64` | Numerical | Organic impressions for Channel 0 |
| 17 | `Promo` | `float64` | Numerical | Promotional activity indicator |
| 18 | `conversions` | `float64` | Numerical | Number of conversions/sales |
| 19 | `revenue_per_conversion` | `float64` | Numerical | Average revenue per conversion |
| 20 | `population` | `float64` | Numerical | Population size for geography |

### 3.2 Column Categories

#### **Marketing Channels (5 channels identified):**
1. **Channel 0** (`Channel0_impression`, `Channel0_spend`)
2. **Channel 1** (`Channel1_impression`, `Channel1_spend`)
3. **Channel 2** (`Channel2_impression`, `Channel2_spend`)
4. **Channel 3** (`Channel3_impression`, `Channel3_spend`)
5. **Channel 4** (`Channel4_impression`, `Channel4_spend`)

#### **Control Variables:**
- `competitor_sales_control`: External competitive factor
- `sentiment_score_control`: Market sentiment indicator
- `Promo`: Promotional activity level

#### **Business Outcomes:**
- `conversions`: Primary business metric (likely sales/conversions)
- `revenue_per_conversion`: Financial performance indicator

#### **Contextual Variables:**
- `geo`: Geographic segmentation
- `time`: Temporal dimension
- `population`: Market size indicator

## 4. Data Quality Assessment

### 4.1 Missing Values Analysis

| Status | Columns Affected | Total Missing | Percentage |
|--------|------------------|---------------|------------|
| **✅ Perfect** | 0 of 20 | 0 | 0.00% |

**Finding:** The dataset contains **no missing values**, which is exceptional for real-world data but expected for a simulated dataset.

### 4.2 Duplicate Analysis

| Check Type | Duplicate Count | Percentage |
|------------|-----------------|------------|
| **Exact Row Duplicates** | 0 | 0.00% |
| **Key Column Duplicates** | 0 | 0.00% |

**Finding:** No duplicate rows detected, indicating clean data generation.

### 4.3 Data Type Consistency

| Data Type | Count | Percentage | Notes |
|-----------|-------|------------|-------|
| `int64` | 7 | 35% | Integer values (counts, impressions) |
| `float64` | 11 | 55% | Continuous values (spend, revenue, control vars) |
| `object` | 2 | 10% | Categorical/text (geo, time) |

**Observation:** Data types appear appropriate for each variable's expected nature.

## 5. Statistical Summary (Key Variables)

### 5.1 Marketing Spend Variables

| Variable | Count | Mean | Std Dev | Min | 25% | 50% | 75% | Max |
|----------|-------|------|---------|-----|-----|-----|-----|-----|
| `Channel0_spend` | 6,240 | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* |
| `Channel1_spend` | 6,240 | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* |
| `Channel2_spend` | 6,240 | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* |
| `Channel3_spend` | 6,240 | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* |
| `Channel4_spend` | 6,240 | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* | *See note* |

*Note: Actual statistical values are available in the Python inspection output. Summary shows all spend variables have consistent count of observations.*

### 5.2 Business Outcome Variables

| Variable | Observations | Key Characteristics |
|----------|-------------|---------------------|
| `conversions` | 6,240 | Continuous positive values, likely representing sales volume |
| `revenue_per_conversion` | 6,240 | Small decimal values (mean ~0.02), stable distribution |

### 5.3 Control Variables

| Variable | Observations | Purpose |
|----------|-------------|---------|
| `competitor_sales_control` | 6,240 | External competitive influence |
| `sentiment_score_control` | 6,240 | Market sentiment indicator |
| `population` | 6,240 | Market size scaling factor |

## 6. Initial Observations

### 6.1 Strengths
1. **Complete Data**: No missing values simplifies analysis
2. **Clear Structure**: Well-named columns with logical groupings
3. **Simulation Quality**: Appears to be a well-constructed simulated dataset
4. **Variable Balance**: Good mix of marketing, control, and outcome variables
5. **Size**: Sufficient observations (6,240) for robust statistical analysis

### 6.2 Potential Considerations
1. **Time Variable Format**: `time` column is stored as string (`object`) - may need conversion to datetime
2. **Categorical Encoding**: `geo` variable needs encoding for modeling
3. **Scale Differences**: Variables likely have different scales requiring normalization
4. **Channel Structure**: Clear channel-level data enables Marketing Mix Modeling

### 6.3 Data Characteristics for MMM
Based on column names, this dataset appears structured for **Marketing Mix Modeling** with:
- Multiple marketing channels with spend and impression data
- Control variables for external factors
- Outcome variables (conversions, revenue)
- Geographic and temporal dimensions

## 7. Questions for Further Investigation

### 7.1 Data Understanding
1. **What do the channel numbers represent?** (e.g., Channel0 = Google Ads, Channel1 = Facebook Ads)
2. **What time period does the data cover?** Need to parse the `time` column
3. **How many unique geographies?** Need to examine `geo` column values
4. **What are the units?** (e.g., spend in USD, impressions in thousands)

### 7.2 Analytical Considerations
1. **Time Series Nature**: Is this panel data (multiple geographies over time)?
2. **Correlation Structure**: How correlated are different channel spends?
3. **Seasonality**: Are there seasonal patterns in conversions?
4. **Geographic Variation**: How do outcomes vary by geography?

### 7.3 Modeling Preparation
1. **Feature Engineering**: Create lagged variables, rolling averages
2. **Encoding**: One-hot encode `geo`, convert `time` to datetime
3. **Normalization**: Scale variables for model stability
4. **Validation Split**: Time-based split for realistic validation

## 8. Recommendations

### 8.1 Immediate Next Steps
1. **Convert `time` to datetime** for proper time series analysis
2. **Explore `geo` values** to understand geographic segmentation
3. **Calculate basic correlations** between spend and conversions
4. **Visualize distributions** of key variables

### 8.2 Preprocessing Requirements
1. **Datetime Conversion**: `pd.to_datetime(df['time'])`
2. **Categorical Encoding**: One-hot or label encoding for `geo`
3. **Feature Scaling**: Standardize/normalize numerical variables
4. **Train/Test Split**: Time-based split to prevent data leakage

### 8.3 Analysis Pathways
1. **Descriptive Analysis**: Channel performance summary
2. **Correlation Analysis**: Relationships between variables
3. **Time Series Decomposition**: Trend, seasonality, residual analysis
4. **MMM Implementation**: Statistical modeling of channel contributions

## 9. Conclusion

The Google Meridian simulated dataset provides an **excellent foundation** for Marketing Mix Modeling development. The data quality is perfect (no missing values, no duplicates), the structure is logical, and all necessary variables for MMM are present.

**Key advantages for MarketMosaic development:**
- Realistic simulated data that mimics real marketing scenarios
- Multiple marketing channels for comparative analysis
- Control variables for robust modeling
- Geographic and temporal dimensions for sophisticated analysis
- Clean, ready-to-use format requiring minimal preprocessing

**Next Phase Focus:** Data preprocessing, exploratory analysis, and initial model development.

---

**Audit Performed By:** MarketMosaic Data Inspection Module  
**Audit Tool:** `src/inspect_data.py`  
**Audit Date:** November 3, 2026  
**Data Source:** Google Meridian Project (simulated MMM data)