from __future__ import annotations

import json
from pathlib import Path

from team_member_2.api import required_input_fields, score_influencer_payload

ROOT = Path(__file__).resolve().parents[1]


def load_sample(name: str) -> dict:
    with (ROOT / "sample_data" / name).open(encoding="utf-8") as file:
        return json.load(file)


def test_public_api_returns_frontend_safe_payload() -> None:
    result = score_influencer_payload(load_sample("influencer_low_risk.json"))

    json.dumps(result)
    assert_frontend_contract(result)


def test_required_input_fields_are_present_in_samples() -> None:
    sample = load_sample("influencer_high_risk.json")

    missing = [field for field in required_input_fields() if field not in sample]

    assert missing == []


def test_dataset_payload_normalizes_and_scores_valid_creator() -> None:
    result = score_influencer_payload(dataset_payload())

    assert_frontend_contract(result)
    assert result["authenticity_score"] > 0
    assert result["risk_level"] in {"Low", "Medium", "High"}
    assert result["ml_risk"]["fraud_probability"] >= 0


def test_missing_comments_returns_stable_schema_with_warning() -> None:
    payload = dataset_payload()
    payload["comments"] = []

    result = score_influencer_payload(payload)

    assert_frontend_contract(result)
    assert any("Comments are empty" in item for item in result["evidence"])


def test_missing_growth_history_returns_stable_schema_with_warning() -> None:
    payload = dataset_payload()
    payload.pop("creator_growth_history")

    result = score_influencer_payload(payload)

    assert_frontend_contract(result)
    assert any("Growth history is missing" in item for item in result["evidence"])


def test_missing_posts_returns_stable_schema_with_warning() -> None:
    payload = dataset_payload()
    payload["posts"] = []

    result = score_influencer_payload(payload)

    assert_frontend_contract(result)
    assert any("Missing posts" in item for item in result["evidence"])


def test_missing_followers_fails_gracefully() -> None:
    payload = dataset_payload()
    payload["profile"].pop("followersCount")

    result = score_influencer_payload(payload)

    assert_frontend_contract(result)
    assert result["authenticity_score"] == 0
    assert result["risk_level"] == "High"
    assert result["alerts"][0]["type"] == "Validation Error"


def dataset_payload() -> dict:
    return {
        "profile": {
            "creatorId": "creator_001",
            "username": "dataset_creator",
            "followersCount": 50000,
            "previousEngagementRate": 0.052,
            "suspiciousFollowerRatio": 0.06,
            "botFollowerRatio": 0.03,
            "inactiveFollowerRatio": 0.12,
            "audienceGeoMismatchRatio": 0.08,
            "previousAuthenticityScore": 86,
            "postsPerWeekHistory": [3, 3, 4, 3, 4, 3],
        },
        "posts": [
            {"likesCount": 2300, "commentsCount": 120},
            {"likesCount": 2500, "commentsCount": 140},
        ],
        "comments": [
            {"text": "Love this review"},
            {"text": "Great breakdown"},
        ],
        "creator_growth_history": {
            "history": [
                {"date": "2026-06-14", "followers": 45000},
                {"date": "2026-06-15", "followers": 45600},
                {"date": "2026-06-16", "followers": 46250},
                {"date": "2026-06-17", "followers": 47000},
                {"date": "2026-06-18", "followers": 47800},
                {"date": "2026-06-19", "followers": 48600},
                {"date": "2026-06-20", "followers": 50000},
            ]
        },
        "campaign": {
            "budget": 10000,
            "expected_reach": 30000,
            "cpm": 12,
        },
    }


def assert_frontend_contract(result: dict) -> None:
    assert set(result) == {
        "authenticity_score",
        "risk_level",
        "evidence",
        "campaign_risk",
        "ml_risk",
        "alerts",
    }
    assert isinstance(result["authenticity_score"], int)
    assert result["risk_level"] in {"Low", "Medium", "High"}
    assert isinstance(result["evidence"], list)
    assert isinstance(result["campaign_risk"], dict)
    assert isinstance(result["ml_risk"], dict)
    assert isinstance(result["alerts"], list)
    assert "fraud_probability" in result["ml_risk"]
    assert "estimated_loss" in result["campaign_risk"]
