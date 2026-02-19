from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv


@dataclass(frozen=True)
class SeedRestaurant:
    name: str
    city: str
    source: str
    source_url: str | None = None


CURATED_NYC = [
    "Atomix", "Le Bernardin", "Tatiana", "Semma", "Don Angie",
    "Lilia", "Via Carota", "4 Charles Prime Rib", "Sushi Noz", "Carbone",
    "Torrisi", "Laser Wolf", "Katz's Delicatessen", "Cote", "Dhamaka",
]

CURATED_PHL = [
    "Zahav", "Vetri Cucina", "Kalaya", "Friday Saturday Sunday", "Laser Wolf Philadelphia",
    "Suraya", "Royal Sushi & Izakaya", "Fork", "Vernick Food & Drink", "Mawn",
    "Fiorella", "Parc", "Honeysuckle Provisions", "Her Place Supper Club", "Middle Child Clubhouse",
]


def built_in_seeds() -> list[SeedRestaurant]:
    records: list[SeedRestaurant] = []
    for name in CURATED_NYC:
        records.append(SeedRestaurant(name=name, city="NYC", source="seed"))
    for name in CURATED_PHL:
        records.append(SeedRestaurant(name=name, city="PHL", source="seed"))
    return records


def load_seed_csv(path: str | Path) -> list[SeedRestaurant]:
    seeds: list[SeedRestaurant] = []
    with Path(path).open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            seeds.append(
                SeedRestaurant(
                    name=row["name"].strip(),
                    city=row["city"].strip().upper(),
                    source="seed_csv",
                    source_url=row.get("source_url", "").strip() or None,
                )
            )
    return seeds
