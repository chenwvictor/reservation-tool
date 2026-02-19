from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlmodel import Session

from resy_sniper.config import settings
from resy_sniper.ingest_seeds import ingest_builtins, normalize_name
from resy_sniper.models import Evidence, Restaurant
from resy_sniper.providers import OpenTableAdapter, ResyAdapter


def fetch_reddit_mentions(city: str) -> list[dict]:
    # TODO: wire PRAW when user provides credentials. Keep respectful rate limits.
    # Fallback placeholder data for local/dev testing.
    now = datetime.utcnow().isoformat()
    return [
        {
            "name": "Atomix" if city == "NYC" else "Zahav",
            "city": city,
            "url": "https://reddit.com/example",
            "snippet": f"I heard this place drops 14 days out at 10:00 ({now})",
            "source": "reddit",
        }
    ]


def merge_mentions(session: Session, mentions: Iterable[dict]) -> int:
    count = 0
    resy = ResyAdapter(settings.resy_api_key, settings.resy_api_base_url)
    opentable = OpenTableAdapter(settings.opentable_api_key, settings.opentable_api_base_url)
    for mention in mentions:
        normalized = normalize_name(mention["name"])
        restaurant = session.query(Restaurant).filter_by(normalized_name=normalized, city=mention["city"]).first()
        if not restaurant:
            provider_match = resy.search(mention["name"], mention["city"])
            if not provider_match.canonical_url:
                provider_match = opentable.search(mention["name"], mention["city"])
            restaurant = Restaurant(
                name=mention["name"],
                normalized_name=normalized,
                city=mention["city"],
                source=mention.get("source", "reddit"),
                provider=provider_match.provider,
                provider_url=provider_match.canonical_url,
            )
            session.add(restaurant)
            session.flush()
        session.add(
            Evidence(
                restaurant_id=restaurant.id,
                source_type=mention.get("source", "reddit"),
                source_url=mention.get("url"),
                snippet=mention["snippet"],
                weight=settings.weight_reddit_match,
            )
        )
        count += 1
    session.commit()
    return count


def run_discovery(session: Session, city: str | None = None) -> dict:
    city = city or settings.default_city
    seed_inserted = ingest_builtins(session)
    mentions = fetch_reddit_mentions(city)
    merged = merge_mentions(session, mentions)
    return {"seed_inserted": seed_inserted, "mentions_merged": merged}
