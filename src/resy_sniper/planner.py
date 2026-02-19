from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from .models import DropRule


def compute_drop_datetime(rule: DropRule, target_date: date) -> datetime:
    tz = ZoneInfo(rule.timezone)
    lead = rule.lead_time_days or 0
    drop_date = target_date - timedelta(days=lead)
    hh, mm = (rule.open_time_local or "09:00").split(":")
    return datetime.combine(drop_date, time(int(hh), int(mm)), tzinfo=tz)
