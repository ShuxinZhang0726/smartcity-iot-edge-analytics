"""Run the reproducible smart city IoT edge-cloud analytics experiment."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from baseline import run_cloud_only_baseline
from data_generator import GeneratorConfig, generate_iot_data
from evaluation import compare_methods
from model import run_edge_cloud_synergy
from visualization import plot_latency_distribution, plot_metric_comparison


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart city IoT edge-cloud analytics experiment")
    parser.add_argument("--sensors", type=int, default=120, help="Number of synthetic sensors")
    parser.add_argument("--minutes", type=int, default=720, help="Number of minutes to simulate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output-dir", type=str, default=str(ROOT / "outputs"), help="Output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cfg = GeneratorConfig(n_sensors=args.sensors, minutes=args.minutes, seed=args.seed)
    data = generate_iot_data(cfg)
    data.to_csv(output_dir / "synthetic_iot.csv", index=False)

    baseline = run_cloud_only_baseline(data)
    improved = run_edge_cloud_synergy(data, seed=args.seed)

    baseline.to_csv(output_dir / "baseline_results.csv", index=False)
    improved.to_csv(output_dir / "improved_results.csv", index=False)

    metrics = compare_methods(baseline, improved)
    metrics.to_csv(output_dir / "metrics.csv", index=False)
    plot_metric_comparison(metrics, output_dir=str(output_dir))
    plot_latency_distribution(baseline, improved, output_dir=str(output_dir))

    print("\nExperiment completed. Metrics:\n")
    print(metrics.round(4).to_string(index=False))
    print(f"\nOutputs saved to: {output_dir}")


if __name__ == "__main__":
    main()
