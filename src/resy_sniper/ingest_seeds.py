from __future__ import annotations

from sqlmodel import select

from resy_sniper.models import Restaurant
from resy_sniper.seeds import SeedRestaurant, built_in_seeds, load_seed_csv


def normalize_name(name: str) -> str:
    return " ".join(name.lower().strip().split())


def upsert_seeds(session, seeds: list[SeedRestaurant]) -> int:
    inserted = 0
    for seed in seeds:
        normalized = normalize_name(seed.name)
        existing = session.exec(
            select(Restaurant).where(
                Restaurant.normalized_name == normalized,
                Restaurant.city == seed.city,
            )
        ).first()
        if existing:
            if seed.source not in existing.source:
                existing.source = f"{existing.source},{seed.source}"
            continue
        session.add(
            Restaurant(
                name=seed.name,
                normalized_name=normalized,
                city=seed.city,
                source=seed.source,
                provider_url=seed.source_url,
            )
        )
        inserted += 1
    session.commit()
    return inserted


def ingest_builtins(session) -> int:
    return upsert_seeds(session, built_in_seeds())


def ingest_csv(session, csv_path: str) -> int:
    return upsert_seeds(session, load_seed_csv(csv_path))
