"""Alert generation for material campaign risks."""

from __future__ import annotations

from schemas import DetectorResult, InfluencerData
from utils.math_utils import as_number


class AlertEngine:
    """Create alert records from detector metrics and score changes."""

    @staticmethod
    def generate(
        data: InfluencerData,
        authenticity_score: int,
        detector_outputs: dict[str, DetectorResult],
    ) -> list[dict[str, str]]:
        """Return alert dictionaries with type, severity, and message."""

        alerts: list[dict[str, str]] = []
        growth = detector_outputs["growth"]["metrics"]
        engagement = detector_outputs["engagement"]["metrics"]
        comments = detector_outputs["comment"]["metrics"]
        previous_score = data.get("previous_authenticity_score")

        if as_number(growth.get("max_daily_growth_rate")) > 0.12:
            alerts.append(
                {
                    "type": "Follower Spike",
                    "severity": "High",
                    "message": "Follower growth spike may indicate purchased followers.",
                }
            )

        if as_number(engagement.get("engagement_drop_rate")) > 0.30:
            alerts.append(
                {
                    "type": "Engagement Drop",
                    "severity": "Medium",
                    "message": "Engagement dropped materially from the previous baseline.",
                }
            )

        if as_number(comments.get("spam_comment_ratio")) > 0.15:
            alerts.append(
                {
                    "type": "Spam Comments",
                    "severity": "Medium",
                    "message": "Recent comments contain spam-like or promotional patterns.",
                }
            )

        if previous_score is not None and as_number(previous_score) - authenticity_score >= 10:
            alerts.append(
                {
                    "type": "Authenticity Drop",
                    "severity": "High",
                    "message": "Authenticity score dropped by at least 10 points.",
                }
            )

        return alerts

