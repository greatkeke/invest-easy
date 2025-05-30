from functools import lru_cache
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging


class Settings(BaseSettings):
    allow_origins: str = "*"  # Default value, will be overridden by .env
    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "../env/.env")),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def allow_origins_list(self) -> List[str]:
        list = [origin.strip() for origin in self.allow_origins.split(",")]
        for item in list:
            logging.warning(f"Allow origin: {item}")
        return list


@lru_cache
def get_settings():
    settings = Settings()
    logging.info(f"Current allow_origins value: {settings.allow_origins}")
    if settings.allow_origins == "*":
        logging.warning(
            "Using default allow_origins value - check .env file configuration"
        )
    return settings


settings = get_settings()
