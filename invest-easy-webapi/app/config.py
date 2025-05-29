from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    allow_origins: str = "*"

    @property
    def allow_origins_list(self) -> List[str]:
        list = [origin.strip() for origin in self.allow_origins.split(",")]
        for item in list:
            logging.info(f"Allow origin: {item}")
        return list


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
