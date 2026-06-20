"""Normalize creator dataset records into the fraud engine schema."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from team_member_2.schemas import InfluencerData
from team_member_2.utils.math_utils import as_number, safe_divide


def normalize_creator_payload(payload: Mapping[str, Any]) -> tuple[InfluencerData, list[str]]:
    """Convert raw dataset or already-normalized payloads into engine input.

    Supported raw fields include:
    - profiles.json style: followersCount
    - posts.json style: likesCount, commentsCount
    - comments.json style: text
    - creator_growth_history.json style: history[].followers
    """

    warnings: list[str] = []
    profile = _first_mapping(payload.get("profile") or payload.get("creator") or payload)
    posts = _as_list(payload.get("posts"))
    comments = _as_list(payload.get("comments"))
    growth = payload.get("creator_growth_history") or payload.get("growth_history") or payload

    followers = _first_number(
        profile,
        "followers",
        "followersCount",
        "followers_count",
        "followerCount",
    )
    normalized_comments = _normalize_comments(payload, comments, warnings)
    follower_history = _normalize_growth_history(payload, growth, warnings)
    average_likes, average_comments = _normalize_post_averages(payload, posts, warnings)

    if followers is None:
        warnings.append("Missing followers value; score returned as validation error.")
        followers = 0

    engagement_rate = _first_number(profile, "engagement_rate", "engagementRate")
    if engagement_rate is None:
        engagement_rate = safe_divide(average_likes + average_comments, followers)

    return (
        {
            "influencer_id": str(
                profile.get("influencer_id")
                or profile.get("creatorId")
                or profile.get("id")
                or ""
            ),
            "username": str(profile.get("username") or profile.get("handle") or ""),
            "followers": int(followers),
            "following": int(_first_number(profile, "following", "followingCount") or 0),
            "average_likes": int(average_likes),
            "average_comments": int(average_comments),
            "engagement_rate": float(engagement_rate),
            "previous_engagement_rate": float(
                _first_number(profile, "previous_engagement_rate", "previousEngagementRate")
                or 0
            ),
            "follower_history": follower_history,
            "posts_per_week_history": _as_number_list(
                profile.get("posts_per_week_history") or profile.get("postsPerWeekHistory")
            ),
            "comments": normalized_comments,
            "suspicious_follower_ratio": float(
                _first_number(profile, "suspicious_follower_ratio", "suspiciousFollowerRatio")
                or 0
            ),
            "bot_follower_ratio": float(
                _first_number(profile, "bot_follower_ratio", "botFollowerRatio") or 0
            ),
            "inactive_follower_ratio": float(
                _first_number(profile, "inactive_follower_ratio", "inactiveFollowerRatio")
                or 0
            ),
            "audience_geo_mismatch_ratio": float(
                _first_number(
                    profile,
                    "audience_geo_mismatch_ratio",
                    "audienceGeoMismatchRatio",
                )
                or 0
            ),
            "previous_authenticity_score": int(
                _first_number(
                    profile,
                    "previous_authenticity_score",
                    "previousAuthenticityScore",
                )
                or 0
            ),
            "campaign": dict(payload.get("campaign") or {}),
        },
        warnings,
    )


def _normalize_post_averages(
    payload: Mapping[str, Any],
    posts: list[Any],
    warnings: list[str],
) -> tuple[float, float]:
    average_likes = _first_number(payload, "average_likes", "averageLikes", "likesCount")
    average_comments = _first_number(
        payload,
        "average_comments",
        "averageComments",
        "commentsCount",
    )

    if posts:
        likes = [
            _first_number(_first_mapping(post), "likesCount", "likes_count", "likes")
            for post in posts
        ]
        comment_counts = [
            _first_number(
                _first_mapping(post),
                "commentsCount",
                "comments_count",
                "comments",
            )
            for post in posts
        ]
        clean_likes = [value for value in likes if value is not None]
        clean_comments = [value for value in comment_counts if value is not None]
        average_likes = sum(clean_likes) / len(clean_likes) if clean_likes else average_likes
        average_comments = (
            sum(clean_comments) / len(clean_comments)
            if clean_comments
            else average_comments
        )
    elif average_likes is None and average_comments is None:
        warnings.append("Missing posts; engagement metrics defaulted to zero.")

    return average_likes or 0, average_comments or 0


def _normalize_comments(
    payload: Mapping[str, Any],
    comments: list[Any],
    warnings: list[str],
) -> list[str]:
    if "comments" in payload and not comments:
        warnings.append("Comments are empty; comment quality confidence reduced.")
        return []

    if comments:
        normalized = []
        for comment in comments:
            if isinstance(comment, str):
                normalized.append(comment)
            elif isinstance(comment, Mapping):
                text = comment.get("text") or comment.get("commentText") or comment.get("body")
                if text:
                    normalized.append(str(text))
        if not normalized:
            warnings.append("Comments are empty; comment quality confidence reduced.")
        return normalized

    direct_comments = payload.get("comment_texts") or payload.get("commentTexts")
    direct_list = [str(item) for item in _as_list(direct_comments) if item]
    if not direct_list:
        warnings.append("Comments are missing; comment quality confidence reduced.")
    return direct_list


def _normalize_growth_history(
    payload: Mapping[str, Any],
    growth: Any,
    warnings: list[str],
) -> list[int]:
    if "follower_history" in payload:
        history = [int(value) for value in _as_number_list(payload.get("follower_history"))]
        if not history:
            warnings.append("Growth history is empty; growth confidence reduced.")
        return history

    growth_mapping = _first_mapping(growth)
    raw_history = growth_mapping.get("history") if growth_mapping else None
    if raw_history is None and isinstance(growth, Sequence) and not isinstance(growth, str):
        raw_history = growth

    history: list[int] = []
    for item in _as_list(raw_history):
        if isinstance(item, Mapping):
            followers = _first_number(item, "followers", "followersCount", "followers_count")
            if followers is not None:
                history.append(int(followers))
        else:
            value = as_number(item, default=-1)
            if value >= 0:
                history.append(int(value))

    if not history:
        warnings.append("Growth history is missing; growth confidence reduced.")
    return history


def _first_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if isinstance(value, Sequence) and not isinstance(value, str) and value:
        first = value[0]
        if isinstance(first, Mapping):
            return first
    return {}


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _as_number_list(value: Any) -> list[float]:
    numbers: list[float] = []
    for item in _as_list(value):
        number = as_number(item, default=-1)
        if number >= 0:
            numbers.append(number)
    return numbers


def _first_number(source: Mapping[str, Any], *keys: str) -> float | None:
    for key in keys:
        if key in source and source[key] is not None:
            return as_number(source[key])
    return None

