"""Base detector contract and common helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from team_member_2.schemas import DetectorResult, InfluencerData
from team_member_2.utils.math_utils import clamp


class BaseDetector(ABC):
    """Base class for all fraud detectors.

    Subclasses must return exactly the standard contract:
    {"score": int, "signals": list, "metrics": dict}.
    """

    name: str

    @abstractmethod
    def analyze(self, data: InfluencerData) -> DetectorResult:
        """Analyze influencer data and return detector evidence."""

    def result(
        self,
        score: float,
        signals: list[str] | None = None,
        metrics: dict[str, Any] | None = None,
    ) -> DetectorResult:
        """Build a normalized detector result."""

        return {
            "score": int(round(clamp(score))),
            "signals": signals or [],
            "metrics": metrics or {},
        }

