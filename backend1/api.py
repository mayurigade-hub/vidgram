"""Public integration facade for backend and frontend consumers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from team_member_2.engines.scoring_engine import ScoringEngine
from team_member_2.normalization import normalize_creator_payload
from team_member_2.schemas import ScoringResult

PUBLIC_OUTPUT_KEYS = (
    "authenticity_score",
    "risk_level",
    "evidence",
    "campaign_risk",
    "ml_risk",
    "alerts",
)


def score_influencer_payload(payload: Mapping[str, Any]) -> ScoringResult:
    """Score a normalized or raw dataset-shaped creator payload.

    Backend2 should call only this facade. The return value keeps stable keys
    for frontend rendering and fails gracefully on invalid input.
    """

    try:
        normalized, warnings = normalize_creator_payload(payload)
        if normalized["followers"] <= 0:
            return _validation_error_response(warnings)

        result = ScoringEngine().score(normalized)
        public_result = _public_response(result)
        if warnings:
            public_result["evidence"] = [
                *(f"Input Warning: {warning}" for warning in warnings),
                *public_result["evidence"],
            ]
        return public_result
    except Exception as exc:  # Defensive API boundary for Backend2.
        return _validation_error_response([f"Unable to analyze creator payload: {exc}"])


def required_input_fields() -> list[str]:
    """Return the minimal fields recommended for reliable scoring."""

    return [
        "followers",
        "average_likes",
        "average_comments",
        "engagement_rate",
        "previous_engagement_rate",
        "follower_history",
        "posts_per_week_history",
        "comments",
        "suspicious_follower_ratio",
        "bot_follower_ratio",
        "inactive_follower_ratio",
        "audience_geo_mismatch_ratio",
        "campaign",
    ]


def _public_response(result: Mapping[str, Any]) -> ScoringResult:
    return {key: result[key] for key in PUBLIC_OUTPUT_KEYS}  # type: ignore[return-value]


def _validation_error_response(errors: list[str]) -> ScoringResult:
    evidence = [f"Validation Error: {error}" for error in errors]
    return {
        "authenticity_score": 0,
        "risk_level": "High",
        "evidence": evidence or ["Validation Error: Invalid creator payload."],
        "campaign_risk": {
            "expected_reach": 0.0,
            "genuine_reach": 0.0,
            "fake_reach": 0.0,
            "fake_reach_ratio": 0.0,
            "estimated_loss": 0.0,
        },
        "ml_risk": {
            "fraud_probability": 0.0,
            "score_adjustment": 0,
            "features": {},
            "explanation": "ML risk was not evaluated because input validation failed.",
        },
        "alerts": [
            {
                "type": "Validation Error",
                "severity": "High",
                "message": error,
            }
            for error in (errors or ["Invalid creator payload."])
        ],
    }
