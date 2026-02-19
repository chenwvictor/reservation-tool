from __future__ import annotations

from datetime import date, datetime, time
from typing import Optional

from sqlmodel import Field, SQLModel


class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    normalized_name: str = Field(index=True)
    city: str = Field(index=True)
    provider: Optional[str] = None
    provider_url: Optional[str] = None
    source: str = "seed"
    popularity_score: float = 0.0


class Evidence(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: Optional[int] = Field(default=None, foreign_key="restaurant.id", index=True)
    source_type: str
    source_url: Optional[str] = None
    snippet: str
    observed_at: datetime = Field(default_factory=datetime.utcnow)
    weight: float = 0.0


class DropRule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id", index=True)
    days_ahead: int = 14
    drop_time: time = Field(default=time(10, 0))
    confidence: float = 0.0
    manual_override: bool = False
    notes: Optional[str] = None


class BookingRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    party_size: int
    target_date: date
    time_window: str
    mode: str = "deeplink"
    status: str = "planned"
    dry_run: bool = True
    profile: Optional[str] = None


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    booking_request_id: int = Field(foreign_key="bookingrequest.id", index=True)
    run_at: datetime
    status: str = "scheduled"
    result: Optional[str] = None
