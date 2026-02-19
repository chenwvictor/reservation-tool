from datetime import date, time

from resy_sniper.planner import compute_drop_datetime


def test_compute_drop_datetime():
    dt = compute_drop_datetime(date(2026, 3, 10), 14, time(10, 0))
    assert dt.isoformat() == "2026-02-24T10:00:00"
