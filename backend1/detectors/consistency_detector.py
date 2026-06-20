"""Posting and performance consistency detector."""

from __future__ import annotations

from statistics import pstdev

from team_member_2.detectors.base import BaseDetector
from team_member_2.schemas import DetectorResult, InfluencerData
from team_member_2.utils.math_utils import average, safe_divide, score_from_penalty


class ConsistencyDetector(BaseDetector):
    """Detect unstable posting cadence that may distort campaign forecasts."""

    name = "consistency"

    def analyze(self, data: InfluencerData) -> DetectorResult:
        posts_per_week = data.get("posts_per_week_history", [])
        signals: list[str] = []

        if len(posts_per_week) < 3:
            return self.result(
                70,
                ["Insufficient posting history; consistency confidence reduced."],
                {"posting_variability": 0.0, "average_posts_per_week": 0.0},
            )

        avg_posts = average(posts_per_week)
        variability = safe_divide(pstdev(posts_per_week), avg_posts)
        penalty = 0.0

        if variability > 0.80:
            penalty += 35
            signals.append(f"Posting cadence is highly inconsistent ({variability:.2f}).")
        elif variability > 0.45:
            penalty += 20
            signals.append(f"Posting cadence is moderately inconsistent ({variability:.2f}).")

        if avg_posts < 1:
            penalty += 15
            signals.append("Average posting cadence is below one post per week.")

        if not signals:
            signals.append("Posting cadence is stable enough for campaign forecasting.")

        return self.result(
            score_from_penalty(penalty),
            signals,
            {
                "posting_variability": round(variability, 4),
                "average_posts_per_week": round(avg_posts, 2),
            },
        )

