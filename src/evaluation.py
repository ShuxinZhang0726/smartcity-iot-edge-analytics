"""Evaluation metrics for latency-aware smart city IoT analytics."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score


def evaluate_method(result: pd.DataFrame) -> dict:
    """Compute accuracy, latency, throughput, and data-movement metrics."""
    y_true = result["event_label"].astype(int)
    y_pred = result["pred_event"].astype(int)
    total_seconds = max((result["timestamp"].max() - result["timestamp"].min()).total_seconds(), 1)
    return {
        "method": result["method"].iloc[0],
        "rows": int(len(result)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "avg_latency_ms": float(result["estimated_latency_ms"].mean()),
        "p95_latency_ms": float(result["estimated_latency_ms"].quantile(0.95)),
        "throughput_msgs_per_sec": float(len(result) / total_seconds),
        "avg_cloud_messages_per_record": float(result["messages_sent_to_cloud"].mean()),
        "avg_edge_compute_ms": float(result["edge_compute_ms"].mean()),
        "avg_cloud_compute_ms": float(result["cloud_compute_ms"].mean()),
    }


def compare_methods(*results: pd.DataFrame) -> pd.DataFrame:
    """Return a comparison table for multiple methods."""
    metrics = [evaluate_method(r) for r in results]
    table = pd.DataFrame(metrics)
    if len(table) >= 2:
        base_latency = table.loc[0, "avg_latency_ms"]
        base_messages = table.loc[0, "avg_cloud_messages_per_record"]
        table["latency_reduction_vs_baseline_pct"] = (base_latency - table["avg_latency_ms"]) / base_latency * 100
        table["cloud_message_reduction_vs_baseline_pct"] = (base_messages - table["avg_cloud_messages_per_record"]) / base_messages * 100
    return table
