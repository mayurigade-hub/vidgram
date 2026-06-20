"""Risk classification engine."""

from __future__ import annotations

from team_member_2.schemas.influencer import RiskLevel


class RiskEngine:
    """Map authenticity scores to business-friendly risk classes."""

    @staticmethod
    def classify(authenticity_score: int) -> RiskLevel:
        """Return Low, Medium, or High risk from a 0-100 score."""

        if authenticity_score >= 75:
            return "Low"
        if authenticity_score >= 50:
            return "Medium"
        return "High"

