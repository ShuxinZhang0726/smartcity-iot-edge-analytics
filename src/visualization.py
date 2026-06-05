"""Visualization utilities for experiment outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_metric_comparison(metrics: pd.DataFrame, output_dir: str = "outputs") -> None:
    """Create simple metric comparison charts."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for metric in ["avg_latency_ms", "p95_latency_ms", "f1", "avg_cloud_messages_per_record"]:
        plt.figure(figsize=(7, 4))
        plt.bar(metrics["method"], metrics[metric])
        plt.title(metric.replace("_", " ").title())
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        plt.savefig(out / f"{metric}.png", dpi=160)
        plt.close()


def plot_latency_distribution(baseline: pd.DataFrame, improved: pd.DataFrame, output_dir: str = "outputs") -> None:
    """Plot latency distributions for both strategies."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 4))
    plt.hist(baseline["estimated_latency_ms"], bins=40, alpha=0.55, label="cloud-only baseline")
    plt.hist(improved["estimated_latency_ms"], bins=40, alpha=0.55, label="edge-cloud improved")
    plt.title("Estimated Latency Distribution")
    plt.xlabel("Latency (ms)")
    plt.ylabel("Record count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "latency_distribution.png", dpi=160)
    plt.close()
