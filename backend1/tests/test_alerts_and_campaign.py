from __future__ import annotations

import json
from pathlib import Path

from team_member_2.engines.scoring_engine import ScoringEngine

ROOT = Path(__file__).resolve().parents[1]


def load_sample(name: str) -> dict:
    with (ROOT / "sample_data" / name).open(encoding="utf-8") as file:
        return json.load(file)


def test_high_risk_alert_generation() -> None:
    result = ScoringEngine().score(load_sample("influencer_high_risk.json"))
    alert_types = {alert["type"] for alert in result["alerts"]}

    assert "Follower Spike" in alert_types
    assert "Engagement Drop" in alert_types
    assert "Spam Comments" in alert_types
    assert "Authenticity Drop" in alert_types


def test_campaign_risk_calculates_reach_and_loss() -> None:
    result = ScoringEngine().score(load_sample("influencer_high_risk.json"))
    campaign_risk = result["campaign_risk"]

    assert campaign_risk["expected_reach"] == 60000
    assert campaign_risk["fake_reach"] > 0
    assert campaign_risk["genuine_reach"] < campaign_risk["expected_reach"]
    assert campaign_risk["fake_reach"] + campaign_risk["genuine_reach"] == campaign_risk["expected_reach"]
    assert campaign_risk["estimated_loss"] > 0

