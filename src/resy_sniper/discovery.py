from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re

from sqlmodel import Session, select

from .models import City, Evidence, Restaurant

DEFAULT_SUBREDDITS = {
    City.NYC: ["FoodNYC", "AskNYC"],
    City.PHL: ["philadelphiaeats", "Philadelphia"],
}

SIGNAL_KEYWORDS = [
    "hard to book",
    "impossible",
    "booked out",
    "sold out",
    "drops",
    "release",
    "opens",
    "available at",
    "21 days",
    "14 days",
]


@dataclass
class RedditItem:
    city: City
    restaurant_name: str
    url: str
    excerpt: str
    posted_at: datetime


def _mock_fetch() -> list[RedditItem]:
    now = datetime.utcnow()
    return [
        RedditItem(City.NYC, "Tatiana", "https://reddit.com/mock1", "Tatiana drops at 10am 21 days out on Resy", now),
        RedditItem(City.PHL, "Vetri Cucina", "https://reddit.com/mock2", "Vetri is impossible; seems to open at 9:00 am two weeks out on OpenTable", now),
    ]


def extract_candidates(text: str) -> bool:
    lower = text.lower()
    return any(k in lower for k in SIGNAL_KEYWORDS)


def refresh_discovery(session: Session) -> int:
    items = _mock_fetch()
    inserted = 0
    for item in items:
        if not extract_candidates(item.excerpt):
            continue
        restaurant = session.exec(select(Restaurant).where(Restaurant.name == item.restaurant_name)).first()
        if not restaurant:
            restaurant = Restaurant(name=item.restaurant_name, city=item.city, popularity_score=1.0)
            session.add(restaurant)
            session.commit()
            session.refresh(restaurant)
            inserted += 1
        evidence = Evidence(
            restaurant_id=restaurant.id,
            url=item.url,
            excerpt=item.excerpt,
            posted_at=item.posted_at,
        )
        session.add(evidence)
    session.commit()
    return inserted
