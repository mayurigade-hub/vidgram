"""Follower growth anomaly detector based on a 7-day rolling window."""

from __future__ import annotations

from detectors.base import BaseDetector
from schemas import DetectorResult, InfluencerData
from utils.math_utils import average, safe_divide, score_from_penalty


class GrowthDetector(BaseDetector):
    """Detect follower spikes using the latest 7 daily follower counts."""

    name = "growth"
    window_days = 7

    def analyze(self, data: InfluencerData) -> DetectorResult:
        raw_history = data.get("follower_history", [])
        history = raw_history[-self.window_days :]
        signals: list[str] = []

        if len(history) < 2:
            return self.result(
                75,
                ["Insufficient 7-day follower history; growth confidence reduced."],
                {
                    "max_daily_growth_rate": 0.0,
                    "average_daily_growth_rate": 0.0,
                    "window_days": len(history),
                    "expected_window_days": self.window_days,
                    "used_latest_window": True,
                },
            )

        growth_rates = [
            safe_divide(history[index] - history[index - 1], history[index - 1])
            for index in range(1, len(history))
            if history[index - 1] > 0
        ]
        max_growth = max(growth_rates, default=0.0)
        avg_growth = average(growth_rates)

        penalty = 0.0
        if max_growth > 0.25:
            penalty += 45
            signals.append(
                f"Follower spike detected: daily growth reached {max_growth:.1%}."
            )
        elif max_growth > 0.12:
            penalty += 25
            signals.append(
                f"Unusual follower growth detected: daily growth reached {max_growth:.1%}."
            )

        if avg_growth > 0.08:
            penalty += 15
            signals.append(f"Average follower growth is elevated at {avg_growth:.1%}.")

        if not signals:
            signals.append("7-day follower growth pattern is within expected range.")

        return self.result(
            score_from_penalty(penalty),
            signals,
            {
                "max_daily_growth_rate": round(max_growth, 4),
                "average_daily_growth_rate": round(avg_growth, 4),
                "window_days": len(history),
                "expected_window_days": self.window_days,
                "used_latest_window": True,
            },
        )
