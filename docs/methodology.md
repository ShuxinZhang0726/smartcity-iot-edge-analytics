# Methodology

## Objective

The project evaluates whether a lightweight edge-cloud architecture can reduce latency and cloud data movement for smart city IoT analytics while retaining useful event-detection performance.

## Data Generation

The synthetic generator creates minute-level readings for four sensor categories:

- Traffic sensors representing road congestion and flow.
- Air quality sensors representing environmental monitoring.
- Energy meters representing urban load patterns.
- Structural sensors representing bridge or public-infrastructure vibration signals.

The generator includes daily patterns, rush-hour effects, random noise, missing values, network jitter, and rare event labels. This produces a controlled environment for method comparison without using private infrastructure data.

## Baseline Method: Cloud-Only Batch ETL

The baseline simulates a conventional centralized workflow:

1. Every raw sensor reading is transmitted to the cloud.
2. Readings wait until a batch ETL window closes.
3. Cloud aggregation and event detection are performed after ingestion.
4. Events are detected using sensor-type-specific rolling z-score thresholds.

This method is intentionally simple and interpretable. It provides a reference point for latency and data movement.

## Improved Method: Edge-Cloud Zero-ETL Synergy

The improved method applies local edge processing before cloud aggregation:

1. Each edge node computes rolling statistics and a priority score.
2. High-priority records are transmitted immediately.
3. Routine records are represented through compact edge summaries.
4. Cloud-side anomaly confirmation is performed on edge summaries using a lightweight Isolation Forest.
5. Estimated latency is computed from edge processing, reduced network transfer, summary-based cloud computation, and minimal zero-ETL overhead.

The method is designed to be practical on a laptop and easy to inspect. It is not a heavy deep learning system.

## Evaluation Metrics

The project reports:

- Precision, recall, and F1 for event-detection quality.
- Average latency and p95 latency.
- Throughput in messages per second.
- Average cloud messages per record.
- Average estimated edge and cloud compute cost.
- Relative latency and cloud-message reduction versus baseline.

## Reproducibility

The experiment is deterministic when a random seed is supplied. The default command is:

```bash
python experiments/run_experiment.py --seed 42
```

All generated data, result tables, and figures are written to the `outputs/` directory.
