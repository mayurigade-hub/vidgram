"""Campaign fraud-adjusted reach and loss calculations."""

from __future__ import annotations

from schemas import DetectorResult, InfluencerData
from utils.math_utils import as_number, clamp, safe_divide


class CampaignRiskEngine:
    """Estimate fake reach, genuine reach, and financial loss."""

    @staticmethod
    def calculate(
        data: InfluencerData,
        authenticity_score: int,
        detector_outputs: dict[str, DetectorResult],
    ) -> dict[str, float]:
        """Return campaign risk estimates from score and audience metrics."""

        campaign = data.get("campaign", {})
        expected_reach = as_number(campaign.get("expected_reach"), as_number(data.get("followers")))
        budget = as_number(campaign.get("budget"))
        cpm = as_number(campaign.get("cpm"))

        audience_metrics = detector_outputs.get("audience_quality", {}).get("metrics", {})
        bad_audience_ratio = as_number(audience_metrics.get("weighted_bad_audience_ratio"))
        score_fake_ratio = 1 - clamp(authenticity_score) / 100
        fake_reach_ratio = clamp(max(score_fake_ratio, bad_audience_ratio), 0, 0.95)

        fake_reach = expected_reach * fake_reach_ratio
        genuine_reach = expected_reach - fake_reach
        loss_from_budget = budget * fake_reach_ratio
        loss_from_cpm = safe_divide(fake_reach, 1000) * cpm if cpm else 0.0
        estimated_loss = max(loss_from_budget, loss_from_cpm)

        return {
            "expected_reach": round(expected_reach, 2),
            "genuine_reach": round(genuine_reach, 2),
            "fake_reach": round(fake_reach, 2),
            "fake_reach_ratio": round(fake_reach_ratio, 4),
            "estimated_loss": round(estimated_loss, 2),
        }

