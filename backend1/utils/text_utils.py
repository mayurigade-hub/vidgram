"""Text helpers for spam and repetition analysis."""

from __future__ import annotations

import re
from collections import Counter

SPAM_KEYWORDS = {
    "buy followers",
    "free followers",
    "promo",
    "dm for collab",
    "check my profile",
    "telegram",
    "whatsapp",
    "giveaway",
}


def normalize_text(value: str) -> str:
    """Lowercase and collapse repeated whitespace for stable comparisons."""

    return re.sub(r"\s+", " ", value.strip().lower())


def spam_ratio(comments: list[str]) -> float:
    """Return the share of comments that look promotional or bot-generated."""

    if not comments:
        return 0.0

    spam_count = 0
    for comment in comments:
        text = normalize_text(comment)
        has_keyword = any(keyword in text for keyword in SPAM_KEYWORDS)
        has_link = "http://" in text or "https://" in text or "www." in text
        has_many_symbols = len(re.findall(r"[!$#@]", text)) >= 4
        if has_keyword or has_link or has_many_symbols:
            spam_count += 1

    return spam_count / len(comments)


def duplicate_ratio(comments: list[str]) -> float:
    """Return the share of repeated comments after normalization."""

    if not comments:
        return 0.0

    normalized = [normalize_text(comment) for comment in comments if comment.strip()]
    if not normalized:
        return 0.0

    counts = Counter(normalized)
    duplicates = sum(count - 1 for count in counts.values() if count > 1)
    return duplicates / len(normalized)

