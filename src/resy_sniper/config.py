from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    db_url: str = os.getenv("RESY_SNIPER_DB", "sqlite:///./resy_sniper.db")
    default_city: str = os.getenv("DEFAULT_CITY", "NYC")

    reddit_user_agent: str = os.getenv("REDDIT_USER_AGENT", "resy-sniper/0.1")
    reddit_client_id: str = os.getenv("REDDIT_CLIENT_ID", "")
    reddit_client_secret: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    reddit_username: str = os.getenv("REDDIT_USERNAME", "")
    reddit_password: str = os.getenv("REDDIT_PASSWORD", "")
    reddit_rate_limit_seconds: int = int(os.getenv("REDDIT_RATE_LIMIT_SECONDS", "2"))

    resy_api_key: str = os.getenv("RESY_API_KEY", "")
    resy_api_base_url: str = os.getenv("RESY_API_BASE_URL", "")
    opentable_api_key: str = os.getenv("OPENTABLE_API_KEY", "")
    opentable_api_base_url: str = os.getenv("OPENTABLE_API_BASE_URL", "")

    weight_seed_bonus: float = float(os.getenv("WEIGHT_SEED_BONUS", "0.5"))
    weight_reddit_match: float = float(os.getenv("WEIGHT_REDDIT_MATCH", "0.3"))
    weight_explicit_pattern: float = float(os.getenv("WEIGHT_EXPLICIT_PATTERN", "0.3"))
    weight_recency_boost: float = float(os.getenv("WEIGHT_RECENCY_BOOST", "0.2"))
    weight_external_signals: float = float(os.getenv("WEIGHT_EXTERNAL_SIGNALS", "0.1"))

    booking_refresh_seconds: int = int(os.getenv("BOOKING_REFRESH_SECONDS", "5"))
    booking_jitter_seconds: int = int(os.getenv("BOOKING_JITTER_SECONDS", "2"))
    profile_storage_enabled: bool = os.getenv("PROFILE_STORAGE_ENABLED", "true").lower() == "true"


settings = Settings()
