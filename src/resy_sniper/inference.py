from __future__ import annotations

import re
from dataclasses import dataclass

from sqlmodel import select

from resy_sniper.config import settings
from resy_sniper.models import DropRule, Evidence, Restaurant

DAYS_PATTERN = re.compile(r"(\d{1,2})\s+days?\s+out", re.IGNORECASE)
TIME_PATTERN = re.compile(r"(?:at|@)\s*(\d{1,2}:\d{2})")
EXPLICIT_PATTERN = re.compile(r"(\d{1,2})\s+days?\s+out\s+(?:at|@)\s*(\d{1,2}:\d{2})", re.IGNORECASE)


@dataclass
class RuleInference:
    days_ahead: int
    drop_time: str
    confidence: float


def parse_rule_from_text(text: str) -> RuleInference | None:
    explicit = EXPLICIT_PATTERN.search(text)
    confidence = 0.0
    if explicit:
        confidence += settings.weight_explicit_pattern
        return RuleInference(int(explicit.group(1)), explicit.group(2), confidence)

    days = DAYS_PATTERN.search(text)
    tmatch = TIME_PATTERN.search(text)
    if not (days and tmatch):
        return None
    return RuleInference(int(days.group(1)), tmatch.group(1), confidence)


def infer_rules(session) -> int:
    created = 0
    restaurants = session.exec(select(Restaurant)).all()
    for restaurant in restaurants:
        evidence_rows = session.exec(select(Evidence).where(Evidence.restaurant_id == restaurant.id)).all()
        matches = [parse_rule_from_text(e.snippet) for e in evidence_rows]
        matches = [m for m in matches if m]
        if not matches:
            continue
        top = matches[0]
        confidence = settings.weight_seed_bonus if "seed" in restaurant.source else 0.0
        confidence += len(matches) * settings.weight_reddit_match
        confidence += top.confidence
        confidence = min(confidence, 1.0)

        hh, mm = [int(x) for x in top.drop_time.split(":")]
        session.add(
            DropRule(
                restaurant_id=restaurant.id,
                days_ahead=top.days_ahead,
                drop_time=f"{hh:02d}:{mm:02d}:00",
                confidence=confidence,
                notes="Auto-inferred from evidence",
            )
        )
        created += 1
    session.commit()
    return created
