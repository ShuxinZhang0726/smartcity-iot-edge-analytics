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


def test_data_generator_shape_and_columns():
    df = generate_iot_data(GeneratorConfig(n_sensors=5, minutes=10, seed=1))
    assert len(df) == 50
    required = {"timestamp", "sensor_id", "sensor_type", "reading", "network_delay_ms", "event_label"}
    assert required.issubset(df.columns)


def test_methods_produce_metrics():
    df = generate_iot_data(GeneratorConfig(n_sensors=10, minutes=40, seed=2))
    baseline = run_cloud_only_baseline(df)
    improved = run_edge_cloud_synergy(df, seed=2)
    metrics = compare_methods(baseline, improved)
    assert len(metrics) == 2
    assert "avg_latency_ms" in metrics.columns
    assert "f1" in metrics.columns
    assert metrics["avg_latency_ms"].notna().all()
