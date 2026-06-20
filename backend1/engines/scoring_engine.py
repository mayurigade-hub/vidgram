"""Top-level authenticity scoring engine."""

from __future__ import annotations

from collections.abc import Iterable

from detectors import (
    AudienceQualityDetector,
    CommentDetector,
    ConsistencyDetector,
    EngagementDetector,
    GrowthDetector,
)
from detectors.base import BaseDetector
from engines.alert_engine import AlertEngine
from engines.campaign_risk_engine import CampaignRiskEngine
from engines.evidence_engine import EvidenceEngine
from engines.ml_risk_engine import MLRiskEngine
from engines.risk_engine import RiskEngine
from schemas import DetectorResult, InfluencerData, ScoringResult
from utils.math_utils import clamp


class ScoringEngine:
    """Run all detectors and produce VidGram's public risk payload."""

    weights = {
        "growth": 0.20,
        "engagement": 0.25,
        "comment": 0.15,
        "audience_quality": 0.25,
        "consistency": 0.15,
    }

    def __init__(self, detectors: Iterable[BaseDetector] | None = None) -> None:
        self.detectors = list(
            detectors
            or [
                GrowthDetector(),
                EngagementDetector(),
                CommentDetector(),
                AudienceQualityDetector(),
                ConsistencyDetector(),
            ]
        )

    def score(self, data: InfluencerData) -> ScoringResult:
        """Return authenticity score, risk level, evidence, campaign risk, and alerts."""

        detector_outputs = self._run_detectors(data)
        base_score = self._weighted_score(detector_outputs)
        ml_risk = MLRiskEngine.evaluate(detector_outputs)
        authenticity_score = int(round(clamp(base_score + ml_risk["score_adjustment"])))
        risk_level = RiskEngine.classify(authenticity_score)
        evidence = EvidenceEngine.build(detector_outputs)
        evidence.append(f"ML Risk ({ml_risk['fraud_probability']:.0%}): {ml_risk['explanation']}")
        campaign_risk = CampaignRiskEngine.calculate(data, authenticity_score, detector_outputs)
        alerts = AlertEngine.generate(data, authenticity_score, detector_outputs)

        return {
            "authenticity_score": authenticity_score,
            "risk_level": risk_level,
            "evidence": evidence,
            "detector_outputs": detector_outputs,
            "ml_risk": ml_risk,
            "campaign_risk": campaign_risk,
            "alerts": alerts,
        }

    def _run_detectors(self, data: InfluencerData) -> dict[str, DetectorResult]:
        outputs: dict[str, DetectorResult] = {}
        for detector in self.detectors:
            output = detector.analyze(data)
            self._validate_detector_result(detector.name, output)
            outputs[detector.name] = output
        return outputs

    def _weighted_score(self, detector_outputs: dict[str, DetectorResult]) -> int:
        weighted_sum = 0.0
        weight_total = 0.0
        for name, output in detector_outputs.items():
            weight = self.weights.get(name, 0.0)
            weighted_sum += output["score"] * weight
            weight_total += weight

        if weight_total == 0:
            raise ValueError("No detector weights configured.")

        return int(round(clamp(weighted_sum / weight_total)))

    @staticmethod
    def _validate_detector_result(name: str, output: DetectorResult) -> None:
        required_keys = {"score", "signals", "metrics"}
        if set(output.keys()) != required_keys:
            raise ValueError(f"{name} detector returned invalid keys: {output.keys()}")
        if not isinstance(output["score"], int):
            raise TypeError(f"{name} detector score must be int.")
        if not 0 <= output["score"] <= 100:
            raise ValueError(f"{name} detector score must be in 0-100 range.")
        if not isinstance(output["signals"], list):
            raise TypeError(f"{name} detector signals must be a list.")
        if not output["signals"]:
            raise ValueError(f"{name} detector must return at least one signal.")
        if not isinstance(output["metrics"], dict):
            raise TypeError(f"{name} detector metrics must be a dict.")
