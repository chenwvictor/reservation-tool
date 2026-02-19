from datetime import date

from resy_sniper.booking import execute_booking
from resy_sniper.db import get_session, init_db
from resy_sniper.models import BookingRequest, Restaurant


def test_booking_dry_run():
    init_db()
    with get_session() as session:
        r = Restaurant(name="Atomix", normalized_name="atomix", city="NYC", source="seed", provider_url="https://resy.com")
        session.add(r)
        session.commit()
        session.refresh(r)

        br = BookingRequest(
            restaurant_id=r.id,
            party_size=2,
            target_date=date(2026, 3, 10),
            time_window="19:00-20:30",
            dry_run=True,
        )
        session.add(br)
        session.commit()
        session.refresh(br)

        result = execute_booking(session, br.id, assist=True, dry_run=True)
        assert result.status == "dry_run"
