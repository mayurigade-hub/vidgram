"""Audience authenticity detector."""

from __future__ import annotations

from detectors.base import BaseDetector
from schemas import DetectorResult, InfluencerData
from utils.math_utils import as_number, score_from_penalty


class AudienceQualityDetector(BaseDetector):
    """Evaluate suspected fake, bot, inactive, and off-target audience share."""

    name = "audience_quality"

    def analyze(self, data: InfluencerData) -> DetectorResult:
        suspicious = as_number(data.get("suspicious_follower_ratio"))
        bots = as_number(data.get("bot_follower_ratio"))
        inactive = as_number(data.get("inactive_follower_ratio"))
        geo_mismatch = as_number(data.get("audience_geo_mismatch_ratio"))
        weighted_bad_audience = (
            suspicious * 0.35 + bots * 0.30 + inactive * 0.20 + geo_mismatch * 0.15
        )
        signals: list[str] = []
        severe_signal_count = 0

        if suspicious > 0.25:
            severe_signal_count += 1
            signals.append(f"Suspicious follower ratio is high at {suspicious:.1%}.")
        if bots > 0.15:
            severe_signal_count += 1
            signals.append(f"Bot follower ratio is high at {bots:.1%}.")
        if inactive > 0.35:
            severe_signal_count += 1
            signals.append(f"Inactive follower ratio is high at {inactive:.1%}.")
        if geo_mismatch > 0.30:
            severe_signal_count += 1
            signals.append(f"Audience geo mismatch is high at {geo_mismatch:.1%}.")

        if not signals:
            signals.append("Audience quality indicators are within expected range.")

        return self.result(
            score_from_penalty(weighted_bad_audience * 100 + severe_signal_count * 8),
            signals,
            {
                "suspicious_follower_ratio": round(suspicious, 4),
                "bot_follower_ratio": round(bots, 4),
                "inactive_follower_ratio": round(inactive, 4),
                "audience_geo_mismatch_ratio": round(geo_mismatch, 4),
                "weighted_bad_audience_ratio": round(weighted_bad_audience, 4),
                "severe_audience_signal_count": severe_signal_count,
            },
        )
