"""Small numeric helpers used across scoring components."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    """Return *value* bounded to the inclusive range [minimum, maximum]."""

    return max(minimum, min(maximum, value))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divide two numbers without raising on missing or zero denominators."""

    if denominator in (0, 0.0, None):
        return default
    return numerator / denominator


def average(values: Iterable[float], default: float = 0.0) -> float:
    """Return the arithmetic mean for values, or *default* when empty."""

    items = list(values)
    if not items:
        return default
    return sum(items) / len(items)


def as_number(value: Any, default: float = 0.0) -> float:
    """Coerce user/sample data into a float with a safe fallback."""

    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def score_from_penalty(penalty: float) -> int:
    """Convert a fraud penalty into the public 0-100 detector score."""

    return int(round(clamp(100 - penalty)))

