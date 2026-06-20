from __future__ import annotations

import json
from pathlib import Path

from engines.risk_engine import RiskEngine
from engines.scoring_engine import ScoringEngine

ROOT = Path(__file__).resolve().parents[1]


def load_sample(name: str) -> dict:
    with (ROOT / "sample_data" / name).open(encoding="utf-8") as file:
        return json.load(file)


def test_low_risk_payload_matches_public_contract() -> None:
    result = ScoringEngine().score(load_sample("influencer_low_risk.json"))

    assert set(result) == {
        "authenticity_score",
        "risk_level",
        "evidence",
        "detector_outputs",
        "ml_risk",
        "campaign_risk",
        "alerts",
    }
    assert result["authenticity_score"] >= 75
    assert result["risk_level"] == "Low"
    assert result["evidence"]
    assert result["ml_risk"]["fraud_probability"] < 0.5
    assert result["detector_outputs"].keys() == ScoringEngine.weights.keys()


def test_high_risk_payload_flags_bad_influencer() -> None:
    result = ScoringEngine().score(load_sample("influencer_high_risk.json"))

    assert result["authenticity_score"] < 50
    assert result["risk_level"] == "High"
    assert result["ml_risk"]["fraud_probability"] >= 0.6
    assert result["ml_risk"]["score_adjustment"] < 0
    assert len(result["evidence"]) >= 5


def test_ml_risk_evidence_is_human_readable() -> None:
    result = ScoringEngine().score(load_sample("influencer_high_risk.json"))

    assert any("ML fraud probability" in item for item in result["evidence"])


def test_risk_classification_boundaries() -> None:
    assert RiskEngine.classify(90) == "Low"
    assert RiskEngine.classify(75) == "Low"
    assert RiskEngine.classify(74) == "Medium"
    assert RiskEngine.classify(50) == "Medium"
    assert RiskEngine.classify(49) == "High"
