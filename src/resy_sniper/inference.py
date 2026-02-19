from __future__ import annotations

import re
from datetime import datetime

from sqlmodel import Session, select

from .models import DropRule, Evidence, Provider, Restaurant

TIME_RE = re.compile(r"(\d{1,2})(:\d{2})?\s?(am|pm)", re.I)
LEAD_RE = re.compile(r"(\d+)\s?(days|weeks)\s?(out|in advance|ahead)", re.I)

NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}


def detect_provider(text: str) -> Provider:
    t = text.lower()
    if "resy" in t:
        return Provider.RESY
    if "opentable" in t or "open table" in t:
        return Provider.OPENTABLE
    return Provider.UNKNOWN


def parse_time(text: str) -> str | None:
    t = text.lower().replace("noon", "12:00 pm").replace("midnight", "12:00 am")
    m = TIME_RE.search(t)
    if not m:
        return None
    hour = int(m.group(1)) % 12
    minute = m.group(2) or ":00"
    if m.group(3).lower() == "pm":
        hour += 12
    return f"{hour:02d}{minute}"


def parse_lead_days(text: str) -> int | None:
    m = LEAD_RE.search(text)
    if m:
        num = int(m.group(1))
        unit = m.group(2).lower()
        return num * 7 if unit.startswith("week") else num
    lowered = text.lower()
    for w, n in NUMBER_WORDS.items():
        if f"{w} week" in lowered:
            return n * 7
        if f"{w} day" in lowered:
            return n
    return None


def infer_rules(session: Session) -> int:
    restaurants = session.exec(select(Restaurant)).all()
    count = 0
    for restaurant in restaurants:
        ev = session.exec(select(Evidence).where(Evidence.restaurant_id == restaurant.id)).all()
        if not ev:
            continue
        times = [parse_time(e.excerpt) for e in ev if parse_time(e.excerpt)]
        leads = [parse_lead_days(e.excerpt) for e in ev if parse_lead_days(e.excerpt)]
        providers = [detect_provider(e.excerpt) for e in ev]
        conf = 0.2
        if times and leads:
            conf += 0.3
        if len(ev) >= 2:
            conf += 0.2
        if any("morning" in e.excerpt.lower() for e in ev):
            conf -= 0.2
        provider = max(providers, key=providers.count)
        if provider != Provider.UNKNOWN:
            restaurant.provider = provider
            session.add(restaurant)
        rule = session.get(DropRule, restaurant.id)
        if not rule:
            rule = DropRule(restaurant_id=restaurant.id)
        rule.lead_time_days = leads[0] if leads else None
        rule.open_time_local = times[0] if times else None
        rule.rule_text = ev[0].excerpt[:200]
        rule.confidence = max(0.0, min(1.0, conf))
        rule.updated_at = datetime.utcnow()
        session.add(rule)
        count += 1
    session.commit()
    return count
