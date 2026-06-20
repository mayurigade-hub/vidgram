"""Engagement quality detector."""

from __future__ import annotations

from detectors.base import BaseDetector
from schemas import DetectorResult, InfluencerData
from utils.math_utils import as_number, safe_divide, score_from_penalty


class EngagementDetector(BaseDetector):
    """Evaluate engagement rate for suspiciously low or high patterns."""

    name = "engagement"

    def analyze(self, data: InfluencerData) -> DetectorResult:
        followers = as_number(data.get("followers"))
        likes = as_number(data.get("average_likes"))
        comments = as_number(data.get("average_comments"))
        engagement_rate = as_number(
            data.get("engagement_rate"),
            safe_divide(likes + comments, followers),
        )
        previous_rate = as_number(data.get("previous_engagement_rate"))
        drop_rate = safe_divide(previous_rate - engagement_rate, previous_rate)
        signals: list[str] = []
        penalty = 0.0

        if followers <= 0:
            return self.result(
                40,
                ["Follower count is missing or zero; engagement cannot be trusted."],
                {"engagement_rate": 0.0, "engagement_drop_rate": 0.0},
            )

        if engagement_rate < 0.01:
            penalty += 35
            signals.append(f"Engagement rate is very low at {engagement_rate:.2%}.")
        elif engagement_rate < 0.02:
            penalty += 20
            signals.append(f"Engagement rate is below benchmark at {engagement_rate:.2%}.")

        if engagement_rate > 0.20 and followers > 10_000:
            penalty += 20
            signals.append(
                f"Engagement rate is unusually high for audience size at {engagement_rate:.2%}."
            )

        if drop_rate > 0.30:
            penalty += 25
            signals.append(f"Engagement dropped {drop_rate:.1%} from the previous baseline.")

        if not signals:
            signals.append("Engagement rate is consistent with audience size.")

        return self.result(
            score_from_penalty(penalty),
            signals,
            {
                "engagement_rate": round(engagement_rate, 4),
                "engagement_drop_rate": round(max(drop_rate, 0.0), 4),
            },
        )

