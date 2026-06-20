from __future__ import annotations

import json
from pathlib import Path

from detectors import (
    AudienceQualityDetector,
    CommentDetector,
    ConsistencyDetector,
    EngagementDetector,
    GrowthDetector,
)

ROOT = Path(__file__).resolve().parents[1]


def load_sample(name: str) -> dict:
    with (ROOT / "sample_data" / name).open(encoding="utf-8") as file:
        return json.load(file)


def test_all_detectors_return_standard_contract() -> None:
    data = load_sample("influencer_high_risk.json")
    detectors = [
        GrowthDetector(),
        EngagementDetector(),
        CommentDetector(),
        AudienceQualityDetector(),
        ConsistencyDetector(),
    ]

    for detector in detectors:
        result = detector.analyze(data)
        assert set(result) == {"score", "signals", "metrics"}
        assert isinstance(result["score"], int)
        assert 0 <= result["score"] <= 100
        assert isinstance(result["signals"], list)
        assert result["signals"]
        assert isinstance(result["metrics"], dict)


def test_high_risk_data_generates_meaningful_fraud_signals() -> None:
    data = load_sample("influencer_high_risk.json")

    assert any("spike" in signal.lower() for signal in GrowthDetector().analyze(data)["signals"])
    assert any("low" in signal.lower() or "dropped" in signal.lower() for signal in EngagementDetector().analyze(data)["signals"])
    assert any("spam" in signal.lower() for signal in CommentDetector().analyze(data)["signals"])
    assert any("bot" in signal.lower() or "suspicious" in signal.lower() for signal in AudienceQualityDetector().analyze(data)["signals"])
    assert any("inconsistent" in signal.lower() for signal in ConsistencyDetector().analyze(data)["signals"])


def test_growth_detector_uses_latest_7_day_window() -> None:
    data = load_sample("influencer_low_risk.json")
    data["follower_history"] = [
        1000,
        2000,
        3000,
        4000,
        45000,
        45600,
        46250,
        47000,
        47800,
        48600,
        50000,
    ]

    result = GrowthDetector().analyze(data)

    assert result["score"] == 100
    assert result["metrics"]["window_days"] == 7
    assert result["metrics"]["expected_window_days"] == 7
    assert result["metrics"]["used_latest_window"] is True
