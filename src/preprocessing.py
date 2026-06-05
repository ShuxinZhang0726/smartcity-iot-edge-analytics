"""Preprocessing utilities for smart city IoT streams."""

from __future__ import annotations

import pandas as pd


def clean_readings(df: pd.DataFrame) -> pd.DataFrame:
    """Impute missing values using sensor-level forward fill and median fallback."""
    required = {"sensor_id", "timestamp", "reading", "sensor_type"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    clean = df.copy()
    clean["timestamp"] = pd.to_datetime(clean["timestamp"])
    clean = clean.sort_values(["sensor_id", "timestamp"])
    clean["reading"] = clean.groupby("sensor_id")["reading"].ffill()
    type_medians = clean.groupby("sensor_type")["reading"].transform("median")
    clean["reading"] = clean["reading"].fillna(type_medians).fillna(clean["reading"].median())
    return clean.reset_index(drop=True)


def add_stream_features(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """Add rolling features used by baseline and edge-cloud models."""
    enriched = clean_readings(df)
    enriched = enriched.sort_values(["sensor_id", "timestamp"])
    grp = enriched.groupby("sensor_id")["reading"]
    enriched["rolling_mean"] = grp.transform(lambda s: s.rolling(window, min_periods=2).mean())
    enriched["rolling_std"] = grp.transform(lambda s: s.rolling(window, min_periods=2).std())
    enriched["rolling_mean"] = enriched["rolling_mean"].fillna(enriched["reading"])
    enriched["rolling_std"] = enriched["rolling_std"].fillna(0.0)
    enriched["z_score"] = (enriched["reading"] - enriched["rolling_mean"]) / (enriched["rolling_std"] + 1e-6)
    enriched["minute_of_day"] = enriched["timestamp"].dt.hour * 60 + enriched["timestamp"].dt.minute
    enriched["is_peak_hour"] = enriched["timestamp"].dt.hour.isin([7, 8, 9, 16, 17, 18]).astype(int)
    return enriched.reset_index(drop=True)


def aggregate_city_snapshot(df: pd.DataFrame, freq: str = "5min") -> pd.DataFrame:
    """Create a city-level analytical snapshot by type and district."""
    work = clean_readings(df)
    work["bucket"] = work["timestamp"].dt.floor(freq)
    return (
        work.groupby(["bucket", "district", "sensor_type"], as_index=False)
        .agg(
            avg_reading=("reading", "mean"),
            max_reading=("reading", "max"),
            event_count=("event_label", "sum"),
            messages=("sensor_id", "count"),
            avg_network_delay_ms=("network_delay_ms", "mean"),
        )
        .sort_values(["bucket", "district", "sensor_type"])
        .reset_index(drop=True)
    )
