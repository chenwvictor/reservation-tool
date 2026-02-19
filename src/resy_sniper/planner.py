from __future__ import annotations

from datetime import date, datetime, time, timedelta


def compute_drop_datetime(target_date: date, days_ahead: int, drop_time: time) -> datetime:
    return datetime.combine(target_date - timedelta(days=days_ahead), drop_time)
