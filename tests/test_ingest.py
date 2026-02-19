from pathlib import Path

from resy_sniper.db import get_session, init_db
from resy_sniper.ingest_seeds import ingest_csv
from resy_sniper.models import Restaurant
from sqlmodel import select


def test_ingest_csv_dedup(tmp_path: Path):
    init_db()
    csv_file = tmp_path / "seeds.csv"
    csv_file.write_text("name,city,source_url\nAtomix,NYC,https://example.com\nAtomix,NYC,https://example2.com\n")

    with get_session() as session:
        inserted = ingest_csv(session, str(csv_file))
        rows = session.exec(select(Restaurant).where(Restaurant.name == "Atomix")).all()

    assert inserted == 1
    assert len(rows) == 1
