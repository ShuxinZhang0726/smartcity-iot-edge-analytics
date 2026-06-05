# Smart City IoT Edge Analytics

## Project Overview

This repository is a complete research prototype for **ultra-low latency data processing in smart city IoT networks**. It simulates heterogeneous city sensors and compares two analytics strategies:

1. **Baseline:** a conventional cloud-only batch ETL pipeline.
2. **Improved method:** an edge-cloud synergy pipeline with local edge scoring, selective cloud transmission, and zero-ETL-style analytical summaries.

The prototype is designed to be small enough to run on a normal laptop while still demonstrating a serious technical workflow: synthetic data generation, modular processing logic, baseline comparison, improved algorithm design, quantitative evaluation, visualization, and research documentation.

## Research Problem

Smart city IoT networks generate high-volume, heterogeneous, latency-sensitive data from transportation, energy, environmental, and infrastructure systems. Sending every raw message to a central cloud warehouse can increase decision latency and waste bandwidth. This prototype studies a narrow research question:

> Can lightweight edge-cloud coordination reduce analytical latency and cloud data movement while preserving useful event-detection performance for smart city IoT streams?

## Why the Topic Matters

Smart city infrastructure is increasingly relevant to public safety, resilient transportation, energy efficiency, environmental monitoring, and infrastructure maintenance. City agencies and public-sector technology teams need analytical systems that support rapid decisions without relying on heavy centralized pipelines for every sensor reading. A reproducible prototype can help evaluate the tradeoff among latency, cloud workload, and detection quality before deploying more complex systems.

## Repository Structure

```text
smartcity-iot-edge-analytics/
├─ README.md
├─ requirements.txt
├─ LICENSE
├─ .gitignore
├─ src/
│  ├─ data_generator.py
│  ├─ preprocessing.py
│  ├─ baseline.py
│  ├─ model.py
│  ├─ evaluation.py
│  └─ visualization.py
├─ experiments/
│  └─ run_experiment.py
├─ docs/
│  ├─ methodology.md
│  ├─ limitations.md
│  └─ research_positioning.md
└─ tests/
   └─ test_basic.py
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Quick Start

Run the default experiment:

```bash
python experiments/run_experiment.py
```

Run a smaller test-size experiment:

```bash
python experiments/run_experiment.py --sensors 40 --minutes 240 --seed 7
```

Run tests:

```bash
pytest
```

## Methodology Summary

The repository uses a synthetic but structured IoT dataset with traffic, air quality, energy, and structural monitoring sensors. The baseline model sends all raw readings to a central cloud pipeline and evaluates events after batch ETL windows. The improved method performs local edge scoring, prioritizes urgent readings, sends compact edge summaries for routine data, and performs cloud-side anomaly confirmation on aggregate summaries.

The comparison focuses on:

- Precision, recall, and F1 for event detection.
- Average and p95 estimated latency.
- Throughput in messages per second.
- Average cloud messages per record as a proxy for data movement.
- Edge and cloud compute estimates.

## Example Output

After running the experiment, the `outputs/` directory contains:

```text
synthetic_iot.csv
baseline_results.csv
improved_results.csv
metrics.csv
avg_latency_ms.png
p95_latency_ms.png
f1.png
avg_cloud_messages_per_record.png
latency_distribution.png
```

A typical console output will look like:

```text
Experiment completed. Metrics:

              method  rows  precision  recall     f1  avg_latency_ms  p95_latency_ms  throughput_msgs_per_sec  avg_cloud_messages_per_record  avg_edge_compute_ms  avg_cloud_compute_ms  latency_reduction_vs_baseline_pct  cloud_message_reduction_vs_baseline_pct
cloud_only_batch_etl 86400     ...       ...    ...        ...             ...                  ...                         1.0000                 0.0000                 ...                         0.0000                                  0.0000
 edge_cloud_zero_etl 86400     ...       ...    ...        ...             ...                  ...                         ...                    ...                    ...                         ...                                     ...
```

Exact values vary with the random seed and experiment size.

## Limitations

This is a research prototype. It uses synthetic sensor data, simplified latency formulas, and a lightweight model rather than a production streaming engine. It does not claim deployment readiness, validated government adoption, or performance on live city networks.

## Future Work

Future work could integrate open municipal datasets, model inter-edge routing constraints, evaluate privacy-preserving edge aggregation, add adaptive threshold learning, and compare the prototype against real streaming frameworks such as Kafka, Flink, or serverless cloud analytics services.

## Disclaimer

This repository is a research prototype intended for reproducible technical demonstration and methodological exploration. It is not a production smart city platform or an operational public-safety system.
