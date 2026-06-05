"""Improved edge-cloud synergy model for low-latency IoT analytics."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from preprocessing import add_stream_features


def _edge_priority_score(work: pd.DataFrame) -> pd.Series:
    """Compute local edge priority using volatility, sensor importance, and peak context."""
    normalized_z = np.minimum(np.abs(work["z_score"]), 8.0) / 8.0
    volatility = np.minimum(work["rolling_std"] / (work["rolling_mean"].abs() + 1e-6), 1.0)
    priority_weight = work["priority"] / work["priority"].max()
    return 0.45 * normalized_z + 0.25 * volatility + 0.20 * priority_weight + 0.10 * work["is_peak_hour"]


def run_edge_cloud_synergy(df: pd.DataFrame, compression_quantile: float = 0.78, seed: int = 42) -> pd.DataFrame:
    """Run a lightweight edge-cloud analytics strategy.

    The method performs local edge scoring, transmits only high-value messages or
    edge summaries, and uses a compact cloud anomaly detector on aggregated
    features. It approximates zero-ETL analytics by avoiding unnecessary raw data
    movement before city-level analytics.
    """
    work = add_stream_features(df)
    work["edge_bucket"] = work["timestamp"].dt.floor("5min")
    work["edge_priority_score"] = _edge_priority_score(work)

    # Local edge selection: high-priority messages are transmitted immediately;
    # low-priority messages are represented through edge summaries.
    threshold = work.groupby("edge_node")["edge_priority_score"].transform(lambda s: s.quantile(compression_quantile))
    work["send_raw_to_cloud"] = (work["edge_priority_score"] >= threshold).astype(int)

    summary = (
        work.groupby(["edge_bucket", "edge_node", "sensor_type"], as_index=False)
        .agg(
            edge_avg=("reading", "mean"),
            edge_max=("reading", "max"),
            edge_volatility=("rolling_std", "mean"),
            edge_priority=("edge_priority_score", "mean"),
            edge_events=("event_label", "sum"),
            raw_selected=("send_raw_to_cloud", "sum"),
            total_messages=("sensor_id", "count"),
        )
    )

    feature_cols = ["edge_avg", "edge_max", "edge_volatility", "edge_priority", "raw_selected", "total_messages"]
    scaler = StandardScaler()
    X = scaler.fit_transform(summary[feature_cols])
    detector = IsolationForest(n_estimators=80, contamination=0.06, random_state=seed)
    summary["summary_anomaly"] = (detector.fit_predict(X) == -1).astype(int)

    work = work.merge(
        summary[["edge_bucket", "edge_node", "sensor_type", "summary_anomaly", "raw_selected", "total_messages"]],
        on=["edge_bucket", "edge_node", "sensor_type"],
        how="left",
    )

    # Edge immediate detection plus cloud summary confirmation.
    local_event = (work["edge_priority_score"] >= threshold).astype(int)
    work["pred_event"] = np.where((local_event == 1) | (work["summary_anomaly"] == 1), 1, 0)

    edge_compute_ms = 4.5 + 0.08 * work.groupby(["edge_bucket", "edge_node"])["sensor_id"].transform("count")
    cloud_summary_ms = 28 + 0.3 * work.groupby("edge_bucket")["edge_node"].transform("nunique")
    zero_etl_overhead_ms = 12
    immediate_bonus = np.where(work["send_raw_to_cloud"] == 1, 0, 40)

    work["messages_sent_to_cloud"] = work["send_raw_to_cloud"] + (1.0 / work["total_messages"].clip(lower=1))
    work["edge_compute_ms"] = edge_compute_ms
    work["cloud_compute_ms"] = cloud_summary_ms
    work["estimated_latency_ms"] = (
        work["network_delay_ms"] * 0.45 + edge_compute_ms + cloud_summary_ms + zero_etl_overhead_ms + immediate_bonus
    )
    work["method"] = "edge_cloud_zero_etl"
    return work
