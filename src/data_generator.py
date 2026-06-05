"""Synthetic smart city IoT stream generator.

The generator creates heterogeneous sensor readings that resemble a city-scale
IoT deployment: traffic loops, air quality stations, energy meters, and bridge
vibration monitors. It intentionally includes burst periods, missing values,
network jitter, and priority events so that latency-aware edge processing can be
evaluated without relying on private infrastructure data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd


SENSOR_TYPES = ["traffic", "air_quality", "energy", "structure"]
DISTRICTS = ["downtown", "industrial", "residential", "transit", "waterfront"]


@dataclass(frozen=True)
class GeneratorConfig:
    """Configuration for synthetic IoT data generation."""

    n_sensors: int = 120
    minutes: int = 720
    seed: int = 42
    anomaly_rate: float = 0.035
    missing_rate: float = 0.015


def _sensor_inventory(cfg: GeneratorConfig, rng: np.random.Generator) -> pd.DataFrame:
    """Create sensor metadata with heterogeneous types and edge assignments."""
    sensor_ids = [f"S{i:04d}" for i in range(cfg.n_sensors)]
    sensor_types = rng.choice(SENSOR_TYPES, size=cfg.n_sensors, p=[0.34, 0.24, 0.26, 0.16])
    districts = rng.choice(DISTRICTS, size=cfg.n_sensors)
    edge_nodes = [f"edge_{d}" for d in districts]
    priority = np.where(np.isin(sensor_types, ["traffic", "structure"]), 2, 1)
    return pd.DataFrame(
        {
            "sensor_id": sensor_ids,
            "sensor_type": sensor_types,
            "district": districts,
            "edge_node": edge_nodes,
            "priority": priority,
        }
    )


def _base_signal(sensor_type: str, minute: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Generate a realistic periodic signal by sensor class."""
    hour = (minute % 1440) / 60.0
    commute_peak = np.exp(-0.5 * ((hour - 8.0) / 1.6) ** 2) + np.exp(-0.5 * ((hour - 17.5) / 1.8) ** 2)
    daily_wave = np.sin(2 * np.pi * minute / 1440)

    if sensor_type == "traffic":
        signal = 35 + 55 * commute_peak + rng.normal(0, 5, size=len(minute))
    elif sensor_type == "air_quality":
        signal = 18 + 12 * commute_peak + 5 * daily_wave + rng.normal(0, 2.5, size=len(minute))
    elif sensor_type == "energy":
        evening = np.exp(-0.5 * ((hour - 20.0) / 2.2) ** 2)
        signal = 70 + 25 * evening + 15 * np.maximum(daily_wave, 0) + rng.normal(0, 6, size=len(minute))
    else:  # structure
        signal = 0.25 + 0.10 * commute_peak + rng.normal(0, 0.04, size=len(minute))
    return signal


def generate_iot_data(cfg: GeneratorConfig | None = None) -> pd.DataFrame:
    """Generate a reproducible synthetic smart city IoT event table.

    Returns:
        DataFrame with one row per sensor-minute reading. Columns include
        timestamps, sensor metadata, reading values, data quality flags, simulated
        network delay, and a binary event label used for evaluation.
    """
    cfg = cfg or GeneratorConfig()
    rng = np.random.default_rng(cfg.seed)
    inventory = _sensor_inventory(cfg, rng)
    timestamps = pd.date_range("2026-01-01 00:00:00", periods=cfg.minutes, freq="min")
    minute = np.arange(cfg.minutes)

    frames: List[pd.DataFrame] = []
    for _, meta in inventory.iterrows():
        values = _base_signal(meta.sensor_type, minute, rng)
        is_event = rng.random(cfg.minutes) < cfg.anomaly_rate
        event_magnitude = rng.uniform(1.35, 2.4, size=cfg.minutes)
        values = np.where(is_event, values * event_magnitude, values)

        missing = rng.random(cfg.minutes) < cfg.missing_rate
        values = values.astype(float)
        values[missing] = np.nan

        base_network_delay = {
            "traffic": 42,
            "air_quality": 65,
            "energy": 80,
            "structure": 38,
        }[meta.sensor_type]
        network_delay_ms = np.maximum(
            5,
            rng.normal(base_network_delay, base_network_delay * 0.25, size=cfg.minutes),
        )

        frames.append(
            pd.DataFrame(
                {
                    "timestamp": timestamps,
                    "sensor_id": meta.sensor_id,
                    "sensor_type": meta.sensor_type,
                    "district": meta.district,
                    "edge_node": meta.edge_node,
                    "priority": meta.priority,
                    "reading": values,
                    "network_delay_ms": network_delay_ms,
                    "event_label": is_event.astype(int),
                    "missing_flag": missing.astype(int),
                }
            )
        )

    data = pd.concat(frames, ignore_index=True)
    return data.sort_values(["timestamp", "sensor_id"]).reset_index(drop=True)


def save_dataset(path: str, cfg: GeneratorConfig | None = None) -> pd.DataFrame:
    """Generate and save a synthetic IoT dataset."""
    df = generate_iot_data(cfg)
    df.to_csv(path, index=False)
    return df


if __name__ == "__main__":
    save_dataset("outputs/synthetic_iot.csv")
