"""Baseline cloud-only ETL simulation."""

from __future__ import annotations

import numpy as np
import pandas as pd

from preprocessing import add_stream_features


def run_cloud_only_baseline(df: pd.DataFrame, batch_minutes: int = 15) -> pd.DataFrame:
    """Simulate a conventional cloud-only ETL pipeline.

    All raw sensor messages are transmitted to a central cloud warehouse. Events
    are detected after batch ETL windows complete. This provides a reasonable
    baseline for latency-sensitive analytics.
    """
    work = add_stream_features(df)
    work["batch_bucket"] = work["timestamp"].dt.floor(f"{batch_minutes}min")

    # Cloud processing is intentionally delayed by batch waiting time, central
    # ingestion cost, and record-level compute overhead.
    minute_in_batch = work["timestamp"].dt.minute % batch_minutes
    batch_wait_ms = (batch_minutes - minute_in_batch) * 60_000
    cloud_ingest_ms = 180 + 0.012 * len(work)
    compute_ms = 3.0 + 0.05 * work.groupby("batch_bucket")["sensor_id"].transform("count")

    threshold = work.groupby("sensor_type")["z_score"].transform(lambda s: s.quantile(0.965))
    work["pred_event"] = (work["z_score"] > threshold).astype(int)
    work["messages_sent_to_cloud"] = 1
    work["edge_compute_ms"] = 0.0
    work["cloud_compute_ms"] = compute_ms
    work["estimated_latency_ms"] = work["network_delay_ms"] + batch_wait_ms + cloud_ingest_ms + compute_ms
    work["method"] = "cloud_only_batch_etl"
    return work
