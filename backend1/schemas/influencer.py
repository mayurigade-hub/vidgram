"""Typed dictionaries used by the scoring module.

The project intentionally avoids runtime schema dependencies so it remains
simple for hackathon demos while still giving editors and tests a contract.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

RiskLevel = Literal["Low", "Medium", "High"]


class DetectorResult(TypedDict):
    """Standard output contract for every detector."""

    score: int
    signals: list[str]
    metrics: dict[str, Any]


class CampaignData(TypedDict, total=False):
    """Campaign inputs needed for fraud-adjusted reach and loss estimates."""

    budget: float
    expected_reach: int
    cpm: float


class InfluencerData(TypedDict, total=False):
    """Flexible influencer input schema consumed by Team Member 2."""

    influencer_id: str
    username: str
    followers: int
    following: int
    average_likes: int
    average_comments: int
    engagement_rate: float
    previous_engagement_rate: float
    follower_history: list[int]  # Latest daily follower counts; growth uses last 7.
    posts_per_week_history: list[float]
    comments: list[str]
    suspicious_follower_ratio: float
    bot_follower_ratio: float
    inactive_follower_ratio: float
    audience_geo_mismatch_ratio: float
    previous_authenticity_score: int
    campaign: CampaignData


class ScoringResult(TypedDict):
    """Public output returned by the scoring engine."""

    authenticity_score: int
    risk_level: RiskLevel
    evidence: list[str]
    detector_outputs: dict[str, DetectorResult]
    ml_risk: dict[str, Any]
    campaign_risk: dict[str, float]
    alerts: list[dict[str, str]]
