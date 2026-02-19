from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class City(str, Enum):
    NYC = "NYC"
    PHL = "PHL"


class Provider(str, Enum):
    RESY = "resy"
    OPENTABLE = "opentable"
    UNKNOWN = "unknown"


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    NEEDS_USER = "needs_user"


class Restaurant(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    city: City = Field(index=True)
    provider: Provider = Field(default=Provider.UNKNOWN)
    provider_url: str | None = None
    popularity_score: float = 0.0
    tags: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Evidence(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    restaurant_id: int = Field(index=True, foreign_key="restaurant.id")
    source: str = "reddit"
    url: str
    excerpt: str
    posted_at: datetime = Field(default_factory=datetime.utcnow)


class DropRule(SQLModel, table=True):
    restaurant_id: int = Field(primary_key=True, foreign_key="restaurant.id")
    lead_time_days: int | None = None
    open_time_local: str | None = None
    timezone: str = "America/New_York"
    rule_text: str | None = None
    confidence: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class BookingRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    party_size: int
    date_target: date
    time_window_start: str
    time_window_end: str
    mode: str = "deeplink"
    dry_run: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    booking_request_id: int = Field(index=True, foreign_key="bookingrequest.id")
    run_at: datetime = Field(index=True)
    status: JobStatus = Field(default=JobStatus.QUEUED, index=True)
    last_error: str | None = None
    log_path: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
