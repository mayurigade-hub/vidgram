"""Comment quality detector."""

from __future__ import annotations

from detectors.base import BaseDetector
from schemas import DetectorResult, InfluencerData
from utils.math_utils import score_from_penalty
from utils.text_utils import duplicate_ratio, spam_ratio


class CommentDetector(BaseDetector):
    """Detect spammy or duplicated comment patterns."""

    name = "comment"

    def analyze(self, data: InfluencerData) -> DetectorResult:
        comments = data.get("comments", [])
        spam = spam_ratio(comments)
        duplicates = duplicate_ratio(comments)
        signals: list[str] = []
        penalty = 0.0

        if not comments:
            return self.result(
                65,
                ["No recent comments provided; comment quality confidence reduced."],
                {"spam_comment_ratio": 0.0, "duplicate_comment_ratio": 0.0},
            )

        if spam > 0.30:
            penalty += 40
            signals.append(f"Spam-like comments are high at {spam:.1%}.")
        elif spam > 0.15:
            penalty += 20
            signals.append(f"Spam-like comments are elevated at {spam:.1%}.")

        if duplicates > 0.25:
            penalty += 30
            signals.append(f"Repeated comments are high at {duplicates:.1%}.")
        elif duplicates > 0.10:
            penalty += 15
            signals.append(f"Repeated comments are elevated at {duplicates:.1%}.")

        if not signals:
            signals.append("Comment quality appears natural.")

        return self.result(
            score_from_penalty(penalty),
            signals,
            {
                "spam_comment_ratio": round(spam, 4),
                "duplicate_comment_ratio": round(duplicates, 4),
            },
        )

