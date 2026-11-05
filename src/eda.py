"""Reusable exploratory analysis helpers for the MarketMosaic dataset."""

from pathlib import Path
from typing import Dict, Iterable, List, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


CHANNELS = [f"Channel{i}" for i in range(5)]
SPEND_COLUMNS = [f"{channel}_spend" for channel in CHANNELS]
IMPRESSION_COLUMNS = [f"{channel}_impression" for channel in CHANNELS]


def load_and_prepare_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """Load the raw CSV and add a validated datetime column."""
    data = pd.read_csv(file_path)
    data = data.copy()
    data["time_dt"] = pd.to_datetime(data["time"], errors="coerce")
    return data


def descriptive_statistics(
    data: pd.DataFrame, columns: Iterable[str]
) -> pd.DataFrame:
    """Return count, mean, standard deviation, quartiles, minimum, and maximum."""
    return data[list(columns)].describe().T


def data_quality_report(data: pd.DataFrame) -> Dict[str, object]:
    """Return explicit checks used to decide whether the panel is well formed."""
    unnamed = data["Unnamed: 0"]
    expected_index = pd.Series(range(len(data)), index=unnamed.index)
    return {
        "missing_cells": int(data.isna().sum().sum()),
        "exact_duplicates": int(data.duplicated().sum()),
        "geo_time_duplicates": int(data.duplicated(["geo", "time"]).sum()),
        "invalid_dates": int(data["time_dt"].isna().sum()),
        "unnamed_unique": int(unnamed.nunique()),
        "unnamed_min": int(unnamed.min()),
        "unnamed_max": int(unnamed.max()),
        "unnamed_is_zero_based_sequence": bool(unnamed.equals(expected_index)),
        "rows_per_geo": data.groupby("geo").size().to_dict(),
        "periods_per_geo": data.groupby("geo")["time"].nunique().to_dict(),
    }


def channel_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Summarise channel scale, zero activity, and unadjusted outcome correlation."""
    rows: List[Dict[str, object]] = []
    for channel, spend, impression in zip(
        CHANNELS, SPEND_COLUMNS, IMPRESSION_COLUMNS
    ):
        rows.append(
            {
                "channel": channel,
                "spend_mean": data[spend].mean(),
                "spend_median": data[spend].median(),
                "spend_total": data[spend].sum(),
                "impressions_mean": data[impression].mean(),
                "impressions_median": data[impression].median(),
                "impressions_total": data[impression].sum(),
                "zero_activity_rows": int((data[spend] == 0).sum()),
                "spend_conversions_correlation": data[spend].corr(
                    data["conversions"]
                ),
                "impressions_conversions_correlation": data[impression].corr(
                    data["conversions"]
                ),
            }
        )
    return pd.DataFrame(rows).set_index("channel")


def geography_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate conversion, population, and total channel spend by geography."""
    result = data.groupby("geo").agg(
        observations=("geo", "size"),
        conversions_mean=("conversions", "mean"),
        conversions_total=("conversions", "sum"),
        population=("population", "first"),
    )
    result["total_spend"] = data.groupby("geo")[SPEND_COLUMNS].sum().sum(axis=1)
    result["conversions_per_population"] = (
        result["conversions_mean"] / result["population"]
    )
    return result.sort_values("conversions_mean", ascending=False)


def temporal_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the panel into weekly conversion and total-spend observations."""
    weekly = data.groupby("time_dt").agg(
        conversions_total=("conversions", "sum"),
        conversions_mean=("conversions", "mean"),
    )
    weekly["total_spend"] = data.groupby("time_dt")[SPEND_COLUMNS].sum().sum(axis=1)
    return weekly.sort_index()


def correlation_matrix(data: pd.DataFrame) -> pd.DataFrame:
    """Return correlations among channel spends and the conversion outcome."""
    return data[SPEND_COLUMNS + ["conversions"]].corr()


def plot_eda_figures(
    data: pd.DataFrame, output_directory: Union[str, Path]
) -> Dict[str, plt.Figure]:
    """Create and save the five Week 1 visualisations."""
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    figures: Dict[str, plt.Figure] = {}

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(data["conversions"], kde=True, ax=axes[0])
    axes[0].set_title("Distribution of conversions")
    long_spend = data[SPEND_COLUMNS].melt(
        var_name="channel", value_name="spend"
    )
    sns.boxplot(data=long_spend, x="channel", y="spend", ax=axes[1])
    axes[1].set_title("Distribution of channel spend")
    fig.tight_layout()
    fig.savefig(output / "01_distributions.png", dpi=150)
    figures["distributions"] = fig

    fig, ax = plt.subplots(figsize=(10, 5))
    data[SPEND_COLUMNS].sum().plot(kind="bar", ax=ax)
    ax.set_title("Total spend by channel")
    ax.set_ylabel("Total spend")
    fig.tight_layout()
    fig.savefig(output / "02_channel_spend_comparison.png", dpi=150)
    figures["channel_spend"] = fig

    fig, axes = plt.subplots(1, 5, figsize=(20, 4), sharey=True)
    for axis, spend, channel in zip(axes, SPEND_COLUMNS, CHANNELS):
        sns.scatterplot(data=data, x=spend, y="conversions", alpha=0.25, ax=axis)
        axis.set_title(channel)
    fig.suptitle("Channel spend and conversions (unadjusted relationships)")
    fig.tight_layout()
    fig.savefig(output / "03_spend_vs_conversions.png", dpi=150)
    figures["spend_vs_conversions"] = fig

    geo = geography_summary(data).reset_index()
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.barplot(data=geo, x="geo", y="conversions_mean", ax=ax, color="steelblue")
    ax.tick_params(axis="x", rotation=90)
    ax.set_title("Mean conversions by geography")
    fig.tight_layout()
    fig.savefig(output / "04_geography_conversions.png", dpi=150)
    figures["geography_conversions"] = fig

    weekly = temporal_summary(data)
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(weekly.index, weekly["conversions_total"], label="Conversions")
    ax.set_title("Weekly total conversions")
    ax.set_xlabel("Week")
    ax.set_ylabel("Conversions")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output / "05_weekly_conversions.png", dpi=150)
    figures["weekly_conversions"] = fig

    return figures
