# Limitations

This repository is intentionally scoped as a research prototype rather than a production platform.

## Synthetic Data

The sensor data is synthetic. It is designed to mimic realistic patterns such as rush-hour congestion, environmental variation, energy usage cycles, and infrastructure anomalies, but it is not a substitute for validation on live municipal data.

## Simplified Latency Model

Latency is estimated through transparent formulas based on network delay, batch waiting time, edge computation, cloud computation, and zero-ETL overhead. Real deployments would require measurement from actual networking, streaming, and database infrastructure.

## Lightweight Model Choice

The improved method uses rolling statistics, priority scoring, and Isolation Forest. These choices keep the project reproducible on a normal laptop, but they do not represent the full range of possible streaming analytics models.

## No Production Guarantees

The code does not provide fault tolerance, authentication, privacy controls, streaming backpressure, live sensor integration, or public-safety validation. It should not be used as an operational decision system.

## Future Extensions

Useful extensions include open-data benchmarking, privacy-preserving edge aggregation, federated edge learning, adaptive routing, multi-city simulation, and integration with real streaming systems.
