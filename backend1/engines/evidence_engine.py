"""Human-readable evidence generation."""

from __future__ import annotations

from team_member_2.schemas import DetectorResult


class EvidenceEngine:
    """Convert detector outputs into explanations for analysts."""

    @staticmethod
    def build(detector_outputs: dict[str, DetectorResult]) -> list[str]:
        """Return sorted evidence statements from every detector signal."""

        evidence: list[str] = []
        for detector_name, output in detector_outputs.items():
            score = output["score"]
            for signal in output["signals"]:
                evidence.append(f"{detector_name.replace('_', ' ').title()} ({score}/100): {signal}")

        return evidence

