from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="RESY_SNIPER_")

    data_dir: Path = Field(default=Path(".data"))
    database_url: str = Field(default="sqlite:///.data/resy_sniper.db")
    timezone: str = Field(default="America/New_York")
    lookback_days: int = Field(default=365)
    reddit_client_id: str | None = Field(default=None)
    reddit_client_secret: str | None = Field(default=None)
    reddit_user_agent: str = Field(default="resy-sniper/0.1")


settings = Settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
