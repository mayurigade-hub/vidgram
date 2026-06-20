"""Lightweight ML-style fraud probability engine.

This intentionally avoids external dependencies. The coefficients act like a
tiny logistic model and can later be replaced with a trained sklearn model
without changing the scoring engine contract.
"""

from __future__ import annotations

import math
from typing import Any

from team_member_2.schemas import DetectorResult
from team_member_2.utils.math_utils import as_number, clamp


class MLRiskEngine:
    """Predict fraud probability and score adjustment from detector metrics."""

    coefficients = {
        "max_daily_growth_rate": 1.35,
        "average_daily_growth_rate": 0.75,
        "engagement_drop_rate": 1.10,
        "spam_comment_ratio": 1.25,
        "duplicate_comment_ratio": 0.55,
        "bot_follower_ratio": 1.20,
        "suspicious_follower_ratio": 1.00,
        "inactive_follower_ratio": 0.55,
        "posting_variability": 0.35,
    }
    intercept = -2.20

    @classmethod
    def evaluate(cls, detector_outputs: dict[str, DetectorResult]) -> dict[str, Any]:
        """Return fraud probability, score adjustment, and explanation."""

        features = cls._extract_features(detector_outputs)
        linear_score = cls.intercept
        for feature_name, coefficient in cls.coefficients.items():
            linear_score += features[feature_name] * coefficient

        fraud_probability = 1 / (1 + math.exp(-linear_score))
        adjustment = cls._score_adjustment(fraud_probability)

        return {
            "fraud_probability": round(fraud_probability, 4),
            "score_adjustment": adjustment,
            "features": features,
            "explanation": cls._explain(fraud_probability, adjustment),
        }

    @staticmethod
    def _extract_features(detector_outputs: dict[str, DetectorResult]) -> dict[str, float]:
        growth = detector_outputs["growth"]["metrics"]
        engagement = detector_outputs["engagement"]["metrics"]
        comment = detector_outputs["comment"]["metrics"]
        audience = detector_outputs["audience_quality"]["metrics"]
        consistency = detector_outputs["consistency"]["metrics"]

        return {
            "max_daily_growth_rate": clamp(as_number(growth.get("max_daily_growth_rate")), 0, 1),
            "average_daily_growth_rate": clamp(as_number(growth.get("average_daily_growth_rate")), 0, 1),
            "engagement_drop_rate": clamp(as_number(engagement.get("engagement_drop_rate")), 0, 1),
            "spam_comment_ratio": clamp(as_number(comment.get("spam_comment_ratio")), 0, 1),
            "duplicate_comment_ratio": clamp(as_number(comment.get("duplicate_comment_ratio")), 0, 1),
            "bot_follower_ratio": clamp(as_number(audience.get("bot_follower_ratio")), 0, 1),
            "suspicious_follower_ratio": clamp(as_number(audience.get("suspicious_follower_ratio")), 0, 1),
            "inactive_follower_ratio": clamp(as_number(audience.get("inactive_follower_ratio")), 0, 1),
            "posting_variability": clamp(as_number(consistency.get("posting_variability")), 0, 2) / 2,
        }

    @staticmethod
    def _score_adjustment(fraud_probability: float) -> int:
        if fraud_probability >= 0.75:
            return -10
        if fraud_probability >= 0.60:
            return -6
        if fraud_probability >= 0.45:
            return -3
        if fraud_probability <= 0.15:
            return 2
        return 0

    @staticmethod
    def _explain(fraud_probability: float, adjustment: int) -> str:
        percent = f"{fraud_probability:.1%}"
        if adjustment < 0:
            return f"ML fraud probability is {percent}; authenticity score adjusted by {adjustment}."
        if adjustment > 0:
            return f"ML fraud probability is {percent}; authenticity score adjusted by +{adjustment}."
        return f"ML fraud probability is {percent}; no score adjustment applied."

